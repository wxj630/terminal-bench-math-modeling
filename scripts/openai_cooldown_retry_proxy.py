#!/usr/bin/env python3
"""Small OpenAI-compatible proxy that waits through provider cooldowns.

The proxy is intentionally thin: it forwards requests to an upstream OpenAI-style
endpoint, but retries transient 429/5xx responses. When the upstream returns a
`model_cooldown` payload with `reset_seconds`, the proxy sleeps for that duration
before retrying the same request.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Iterable


HOP_BY_HOP_HEADERS = {
    "connection",
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "te",
    "trailers",
    "transfer-encoding",
    "upgrade",
}

RETRY_STATUSES = {429, 500, 502, 503, 504}


def log(message: str) -> None:
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}", file=sys.stderr, flush=True)


def getenv_required(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise SystemExit(f"Missing required environment variable: {name}")
    return value


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default=os.environ.get("PROXY_HOST", "127.0.0.1"))
    parser.add_argument("--port", type=int, default=int(os.environ.get("PROXY_PORT", "30318")))
    parser.add_argument("--upstream-base", default=os.environ.get("UPSTREAM_API_BASE"))
    parser.add_argument("--api-key", default=os.environ.get("UPSTREAM_API_KEY"))
    parser.add_argument("--max-attempts", type=int, default=int(os.environ.get("PROXY_MAX_ATTEMPTS", "80")))
    parser.add_argument("--request-timeout", type=float, default=float(os.environ.get("PROXY_REQUEST_TIMEOUT", "1800")))
    parser.add_argument("--cooldown-padding", type=float, default=float(os.environ.get("PROXY_COOLDOWN_PADDING", "5")))
    parser.add_argument("--chat-template-kwargs", default=os.environ.get("PROXY_CHAT_TEMPLATE_KWARGS"))
    parser.add_argument("--provider-order", default=os.environ.get("PROXY_PROVIDER_ORDER"))
    parser.add_argument("--provider-allow-fallbacks", default=os.environ.get("PROXY_PROVIDER_ALLOW_FALLBACKS"))
    return parser.parse_args()


def strip_v1_prefix(path: str) -> str:
    if path == "/v1":
        return ""
    if path.startswith("/v1/"):
        return path[len("/v1/") :]
    return path.lstrip("/")


def build_upstream_url(upstream_base: str, path: str) -> str:
    parsed = urllib.parse.urlsplit(path)
    suffix = strip_v1_prefix(parsed.path)
    base = upstream_base.rstrip("/") + "/"
    url = urllib.parse.urljoin(base, suffix)
    if parsed.query:
        url = f"{url}?{parsed.query}"
    return url


def copy_headers(headers: Iterable[tuple[str, str]]) -> dict[str, str]:
    copied: dict[str, str] = {}
    for key, value in headers:
        lower = key.lower()
        if lower in HOP_BY_HOP_HEADERS or lower in {"host", "content-length"}:
            continue
        copied[key] = value
    return copied


def error_payload(exc: BaseException) -> bytes:
    payload = {
        "error": {
            "code": "local_proxy_error",
            "message": str(exc),
        }
    }
    return json.dumps(payload).encode("utf-8")


def extract_retry_delay(status: int, body: bytes, attempt: int, padding: float) -> float:
    text = body.decode("utf-8", errors="replace")
    default_delay = min(120.0, max(5.0, 5.0 * attempt))

    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        payload = {}

    error = payload.get("error", {}) if isinstance(payload, dict) else {}
    reset_seconds = error.get("reset_seconds") if isinstance(error, dict) else None
    if reset_seconds is not None:
        try:
            return max(1.0, float(reset_seconds) + padding)
        except (TypeError, ValueError):
            pass

    match = re.search(r'"reset_seconds"\s*:\s*([0-9.]+)', text)
    if match:
        return max(1.0, float(match.group(1)) + padding)

    if isinstance(error, dict) and error.get("code") == "model_cooldown":
        return 120.0 + padding

    if status == 429:
        return 60.0
    return default_delay


class RetryProxy(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    upstream_base: str
    upstream_api_key: str
    max_attempts: int
    request_timeout: float
    cooldown_padding: float
    chat_template_kwargs: dict[str, object] | None
    provider_order: list[str] | None
    provider_allow_fallbacks: bool | None

    def do_GET(self) -> None:
        self._handle()

    def do_POST(self) -> None:
        self._handle()

    def do_HEAD(self) -> None:
        self._handle(send_body=False)

    def log_message(self, format: str, *args: object) -> None:
        log(format % args)

    def _handle(self, send_body: bool = True) -> None:
        body = self._transform_body(self._read_body())
        url = build_upstream_url(self.upstream_base, self.path)
        method = self.command

        last_body = b""
        last_status = 502
        for attempt in range(1, self.max_attempts + 1):
            try:
                status, response_headers, response_body = self._forward(method, url, body)
            except (TimeoutError, urllib.error.URLError, OSError) as exc:
                last_body = error_payload(exc)
                last_status = 502
                delay = min(120.0, max(5.0, 5.0 * attempt))
                log(f"{method} {self.path} attempt {attempt}/{self.max_attempts} failed locally: {exc}; sleeping {delay:.1f}s")
                time.sleep(delay)
                continue

            last_status = status
            last_body = response_body
            if status not in RETRY_STATUSES:
                self._send(status, response_headers, response_body, send_body=send_body)
                return

            if attempt >= self.max_attempts:
                break

            delay = extract_retry_delay(status, response_body, attempt, self.cooldown_padding)
            log(f"{method} {self.path} upstream {status} on attempt {attempt}/{self.max_attempts}; sleeping {delay:.1f}s")
            time.sleep(delay)

        self._send(last_status, {"Content-Type": "application/json"}, last_body, send_body=send_body)

    def _read_body(self) -> bytes | None:
        content_length = self.headers.get("Content-Length")
        if not content_length:
            return None
        return self.rfile.read(int(content_length))

    def _transform_body(self, body: bytes | None) -> bytes | None:
        if body is None or self.command != "POST":
            return body
        if strip_v1_prefix(urllib.parse.urlsplit(self.path).path) != "chat/completions":
            return body
        if self.chat_template_kwargs is None and self.provider_order is None and self.provider_allow_fallbacks is None:
            return body
        try:
            payload = json.loads(body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            return body
        if not isinstance(payload, dict):
            return body
        if self.chat_template_kwargs is not None:
            existing = payload.get("chat_template_kwargs")
            if isinstance(existing, dict):
                existing.update(self.chat_template_kwargs)
            else:
                payload["chat_template_kwargs"] = self.chat_template_kwargs
        if self.provider_order is not None or self.provider_allow_fallbacks is not None:
            provider = payload.get("provider")
            if not isinstance(provider, dict):
                provider = {}
            if self.provider_order is not None:
                provider["order"] = self.provider_order
            if self.provider_allow_fallbacks is not None:
                provider["allow_fallbacks"] = self.provider_allow_fallbacks
            payload["provider"] = provider
        return json.dumps(payload).encode("utf-8")

    def _forward(self, method: str, url: str, body: bytes | None) -> tuple[int, dict[str, str], bytes]:
        headers = copy_headers(self.headers.items())
        headers["Authorization"] = f"Bearer {self.upstream_api_key}"
        request = urllib.request.Request(url, data=body, method=method, headers=headers)
        try:
            with urllib.request.urlopen(request, timeout=self.request_timeout) as response:
                response_body = response.read()
                return response.status, copy_headers(response.headers.items()), response_body
        except urllib.error.HTTPError as exc:
            response_body = exc.read()
            return exc.code, copy_headers(exc.headers.items()), response_body

    def _send(self, status: int, headers: dict[str, str], body: bytes, send_body: bool = True) -> None:
        self.send_response(status)
        for key, value in headers.items():
            if key.lower() in HOP_BY_HOP_HEADERS or key.lower() == "content-length":
                continue
            self.send_header(key, value)
        self.send_header("Content-Length", str(len(body) if send_body else 0))
        try:
            self.end_headers()
            if send_body:
                self.wfile.write(body)
        except BrokenPipeError:
            log(f"Client closed connection before proxy could return upstream status {status}")


def main() -> None:
    args = parse_args()
    RetryProxy.upstream_base = args.upstream_base or getenv_required("UPSTREAM_API_BASE")
    RetryProxy.upstream_api_key = args.api_key or getenv_required("UPSTREAM_API_KEY")
    RetryProxy.max_attempts = args.max_attempts
    RetryProxy.request_timeout = args.request_timeout
    RetryProxy.cooldown_padding = args.cooldown_padding
    if args.chat_template_kwargs:
        try:
            chat_template_kwargs = json.loads(args.chat_template_kwargs)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"Invalid --chat-template-kwargs JSON: {exc}") from exc
        if not isinstance(chat_template_kwargs, dict):
            raise SystemExit("--chat-template-kwargs must be a JSON object")
        RetryProxy.chat_template_kwargs = chat_template_kwargs
    else:
        RetryProxy.chat_template_kwargs = None
    if args.provider_order:
        RetryProxy.provider_order = [item.strip() for item in args.provider_order.split(",") if item.strip()]
    else:
        RetryProxy.provider_order = None
    if args.provider_allow_fallbacks is None:
        RetryProxy.provider_allow_fallbacks = None
    else:
        value = args.provider_allow_fallbacks.strip().lower()
        if value not in {"true", "false"}:
            raise SystemExit("--provider-allow-fallbacks must be true or false")
        RetryProxy.provider_allow_fallbacks = value == "true"

    server = ThreadingHTTPServer((args.host, args.port), RetryProxy)
    log(f"Listening on http://{args.host}:{args.port}/v1 -> {RetryProxy.upstream_base.rstrip('/')}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        log("Stopping")


if __name__ == "__main__":
    main()
