# -*- coding: utf-8 -*-
"""Write geometry visual guide diagrams for TB-MathModeling tasks."""

from __future__ import annotations

from dataclasses import dataclass
from html import escape
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = REPO_ROOT / "docs" / "assets" / "geometry"
GUIDE_PATH = REPO_ROOT / "docs" / "GEOMETRY_VISUAL_GUIDE.md"


@dataclass(frozen=True)
class Figure:
    slug: str
    title: str
    contest: str
    final_question: str
    final_answer: str
    baseline_model: str
    reading_hint: str

    @property
    def filename(self) -> str:
        return f"{self.slug}.svg"


def _text(x: float, y: float, value: str, cls: str = "label", anchor: str = "start") -> str:
    return f'<text x="{x:g}" y="{y:g}" class="{cls}" text-anchor="{anchor}">{escape(value)}</text>'


def _wrapped_text(
    x: float,
    y: float,
    value: str,
    width: int,
    cls: str = "small",
    line_height: int = 18,
    anchor: str = "start",
) -> str:
    def display_width(ch: str) -> float:
        return 0.55 if ord(ch) < 128 else 1.0

    def cjk_wrap(para: str) -> list[str]:
        leading_punctuation = set("，。、；：！？）》】、%")
        wrapped: list[str] = []
        current: list[str] = []
        current_width = 0.0
        for ch in para:
            ch_width = display_width(ch)
            if current and current_width + ch_width > width:
                if ch in leading_punctuation:
                    current.append(ch)
                    wrapped.append("".join(current).rstrip())
                    current = []
                    current_width = 0.0
                else:
                    wrapped.append("".join(current).rstrip())
                    current = [ch.lstrip()]
                    current_width = display_width(current[0]) if current[0] else 0.0
            else:
                current.append(ch)
                current_width += ch_width
        if current:
            wrapped.append("".join(current).rstrip())
        return wrapped

    lines: list[str] = []
    for para in value.split("\n"):
        if not para:
            lines.append("")
            continue
        lines.extend(cjk_wrap(para))
    return "\n".join(
        f'<text x="{x:g}" y="{y + index * line_height:g}" class="{cls}" text-anchor="{anchor}">{escape(line)}</text>'
        for index, line in enumerate(lines)
    )


def _base_svg(title: str, subtitle: str, content: str, *, width: int = 1080, height: int = 560) -> str:
    return "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{escape(title)}">',
            "<defs>",
            '<marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">',
            '<path d="M 0 0 L 10 5 L 0 10 z" fill="#244c7c"/>',
            "</marker>",
            '<marker id="arrow-warm" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">',
            '<path d="M 0 0 L 10 5 L 0 10 z" fill="#b45b18"/>',
            "</marker>",
            '<linearGradient id="water" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#dff3ff"/><stop offset="100%" stop-color="#9cc7d9"/></linearGradient>',
            '<linearGradient id="ground" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#f4efe5"/><stop offset="100%" stop-color="#d7c3a0"/></linearGradient>',
            '<filter id="soft" x="-10%" y="-10%" width="120%" height="120%"><feDropShadow dx="0" dy="2" stdDeviation="2" flood-color="#000" flood-opacity=".12"/></filter>',
            "</defs>",
            "<style>",
            "text{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans CJK SC','Microsoft YaHei',Arial,sans-serif;fill:#1f2933}",
            ".title{font-size:25px;font-weight:700}.subtitle{font-size:14px;fill:#59636e}.label{font-size:15px;font-weight:650}.small{font-size:13px;fill:#3d4852}.value{font-size:14px;font-weight:700;fill:#0f5e57}.muted{font-size:12px;fill:#66788a}.axis{stroke:#415466;stroke-width:2}.thin{stroke:#5f6f80;stroke-width:1.5}.dash{stroke-dasharray:7 6}.blue{stroke:#244c7c}.warm{stroke:#b45b18}.green{stroke:#087f5b}.red{stroke:#b42318}.fill-blue{fill:#e5f1ff}.fill-warm{fill:#fff0df}.fill-green{fill:#e4f7ef}.fill-red{fill:#fff1f0}.panel{fill:#fbfcfd;stroke:#d8dee6;stroke-width:1}.note{fill:#fffdf7;stroke:#e4cf8c;stroke-width:1}",
            "</style>",
            f'<rect x="0" y="0" width="{width}" height="{height}" fill="#ffffff"/>',
            _text(36, 42, title, "title"),
            _text(36, 66, subtitle, "subtitle"),
            content,
            "</svg>",
        ]
    )


def _heliostat() -> str:
    mirrors = []
    for x, y, rot in [
        (190, 250, -12),
        (250, 305, 8),
        (320, 250, 16),
        (395, 310, -6),
        (170, 355, 14),
        (300, 390, -14),
        (430, 380, 10),
    ]:
        mirrors.append(
            f'<g transform="translate({x} {y}) rotate({rot})"><rect x="-24" y="-6" width="48" height="12" fill="#b6d7ff" stroke="#244c7c" stroke-width="1.5"/><line x1="0" y1="6" x2="0" y2="30" class="thin blue"/></g>'
        )
    return _base_svg(
        "CUMCM 2023 A 定日镜场",
        "题面是太阳光反射几何；答案是在 60 MW 附近做高效率镜场设计。",
        "\n".join(
            [
                '<rect x="36" y="92" width="580" height="400" class="panel"/>',
                '<ellipse cx="320" cy="355" rx="230" ry="88" fill="#f5f9ee" stroke="#98a873" stroke-width="2"/>',
                '<ellipse cx="320" cy="355" rx="150" ry="55" fill="none" stroke="#c9d8ad" stroke-width="2" stroke-dasharray="5 5"/>',
                '<rect x="306" y="145" width="28" height="210" fill="#8b95a1" stroke="#46505a"/>',
                '<rect x="286" y="132" width="68" height="18" fill="#ffcf66" stroke="#8a5a00"/>',
                _text(320, 125, "吸收塔/接收器", "label", "middle"),
                '<line x1="92" y1="116" x2="226" y2="240" class="axis warm" marker-end="url(#arrow-warm)"/>',
                '<line x1="70" y1="148" x2="190" y2="253" class="thin warm" marker-end="url(#arrow-warm)"/>',
                '<line x1="226" y1="240" x2="302" y2="145" class="axis blue" marker-end="url(#arrow)"/>',
                '<line x1="190" y1="253" x2="306" y2="148" class="thin blue" marker-end="url(#arrow)"/>',
                _text(92, 104, "太阳入射光", "small"),
                _text(383, 162, "反射到塔顶", "small"),
                *mirrors,
                _text(320, 472, "圆形镜场：镜子位置、面积、高度共同影响阴影/遮挡/余弦效率", "small", "middle"),
                '<rect x="654" y="92" width="374" height="400" class="note"/>',
                _text(676, 128, "最后答案在量什么", "label"),
                _wrapped_text(676, 160, "约束：年平均热功率要接近 60 MW；目标：单位镜面面积输出越高越好，同时镜面面积和镜子数量越少越好。", 22),
                _text(676, 248, "O 奖复现答案", "label"),
                _text(676, 282, "年平均热功率 60.336111 MW", "value"),
                _text(676, 314, "单位面积功率 0.506192417 kW/m2", "value"),
                _text(676, 346, "年平均光学效率 0.496428083", "value"),
                _text(676, 378, "镜面总面积 119196 m2", "value"),
                _text(676, 410, "定日镜 3311 面", "value"),
            ]
        ),
    )


def _multibeam() -> str:
    return _base_svg(
        "CUMCM 2023 B 多波束测线",
        "题面是海底地形上的条带覆盖；答案在平衡航行长度、漏测和重叠。",
        "\n".join(
            [
                '<rect x="36" y="92" width="580" height="400" fill="url(#water)" stroke="#7aa8bd"/>',
                '<polygon points="70,400 570,320 570,455 70,455" fill="#c2a378" stroke="#896b42"/>',
                _text(90, 432, "倾斜海底", "small"),
                '<line x1="115" y1="125" x2="115" y2="400" class="axis blue" marker-end="url(#arrow)"/>',
                '<line x1="210" y1="125" x2="210" y2="385" class="axis blue" marker-end="url(#arrow)"/>',
                '<line x1="305" y1="125" x2="305" y2="370" class="axis blue" marker-end="url(#arrow)"/>',
                '<line x1="400" y1="125" x2="400" y2="354" class="axis blue" marker-end="url(#arrow)"/>',
                '<line x1="495" y1="125" x2="495" y2="339" class="axis blue" marker-end="url(#arrow)"/>',
                '<polygon points="115,400 56,449 174,430" fill="#d7ebff" stroke="#244c7c" opacity=".8"/>',
                '<polygon points="210,385 148,437 272,417" fill="#d7ebff" stroke="#244c7c" opacity=".8"/>',
                '<polygon points="305,370 238,424 372,402" fill="#d7ebff" stroke="#244c7c" opacity=".8"/>',
                '<polygon points="400,354 330,411 470,389" fill="#d7ebff" stroke="#244c7c" opacity=".8"/>',
                '<polygon points="495,339 424,397 566,374" fill="#d7ebff" stroke="#244c7c" opacity=".8"/>',
                '<path d="M156 438 L174 430 L148 437 Z" fill="#f7d794" stroke="#b45b18"/>',
                '<path d="M250 422 L272 417 L238 424 Z" fill="#f7d794" stroke="#b45b18"/>',
                '<path d="M348 406 L372 402 L330 411 Z" fill="#f7d794" stroke="#b45b18"/>',
                _text(84, 116, "测线", "small"),
                _text(253, 475, "相邻条带要覆盖全海域，但过多重叠也浪费", "small", "middle"),
                '<rect x="654" y="92" width="374" height="400" class="note"/>',
                _text(676, 128, "最后答案在量什么", "label"),
                _wrapped_text(676, 160, "真实海深数据给出以后，要规划测线。总航行长度和漏测面积越小越好；平均重叠率要受控，重叠超过 20% 的长度越少越好。", 22),
                _text(676, 264, "O 奖复现方案", "label"),
                _text(676, 298, "总测线长度 622.0 海里", "value"),
                _text(676, 330, "漏测面积 3.48%", "value"),
                _text(676, 362, "重叠>20% 长度 30.0 海里", "value"),
                _text(676, 394, "平均重叠率 10.48%", "value"),
            ]
        ),
    )


def _dragon() -> str:
    spiral = "M330 315 C300 280 310 230 355 210 C420 182 495 220 500 285 C506 360 420 418 342 382 C258 344 230 242 294 168 C372 78 530 103 584 204"
    benches = []
    for x, y, rot in [
        (330, 315, 32),
        (366, 286, -8),
        (408, 271, -36),
        (452, 289, 24),
        (469, 334, 63),
        (438, 370, -30),
        (384, 379, -10),
        (322, 356, 20),
    ]:
        benches.append(
            f'<g transform="translate({x} {y}) rotate({rot})"><rect x="-32" y="-8" width="64" height="16" rx="3" fill="#ffe1bf" stroke="#b45b18"/><circle cx="-23" cy="0" r="3" fill="#244c7c"/><circle cx="23" cy="0" r="3" fill="#244c7c"/></g>'
        )
    return _base_svg(
        "CUMCM 2024 A 板凳龙调头",
        "题面是把一串刚性板凳约束在螺线/调头曲线上；答案是速度安全上限。",
        "\n".join(
            [
                '<rect x="36" y="92" width="580" height="400" class="panel"/>',
                f'<path d="{spiral}" fill="none" stroke="#244c7c" stroke-width="4" marker-end="url(#arrow)"/>',
                '<path d="M328 318 C280 380 208 354 195 292 C183 234 229 184 294 168" fill="none" stroke="#087f5b" stroke-width="3" stroke-dasharray="7 6" marker-end="url(#arrow)"/>',
                '<circle cx="330" cy="315" r="68" fill="none" stroke="#9fb8c9" stroke-dasharray="6 6"/>',
                '<circle cx="330" cy="315" r="6" fill="#b42318"/>',
                *benches,
                _text(582, 202, "盘入/盘出螺线", "small", "end"),
                _text(205, 250, "调头曲线", "small"),
                _text(330, 466, "每块板凳由相邻把手距离约束，头部速度会传到整条龙", "small", "middle"),
                '<rect x="654" y="92" width="374" height="400" class="note"/>',
                _text(676, 128, "最后答案在量什么", "label"),
                _wrapped_text(676, 160, "沿最终调头路径行进时，所有把手速度都不能超过 2 m/s。需要反推出龙头能保持的最大匀速。", 22),
                _text(676, 248, "O 奖复现答案", "label"),
                _text(676, 282, "龙头最大速度 2.00002 m/s", "value"),
                _text(676, 314, "若龙头 1 m/s，最大速度比例 0.99999", "value"),
                _text(676, 360, "方向：最大可行速度越高越好；速度放大比例越低越安全。", "small"),
            ]
        ),
    )


def _smoke() -> str:
    return _base_svg(
        "CUMCM 2025 A 烟幕遮蔽",
        "题面是三维轨迹和视线遮挡；答案是三枚导弹被烟幕有效遮蔽的联合时长。",
        "\n".join(
            [
                '<rect x="36" y="92" width="580" height="400" class="panel"/>',
                '<polygon points="55,420 585,420 545,480 95,480" fill="#eef2f6" stroke="#c9d2dc"/>',
                '<rect x="465" y="334" width="44" height="86" fill="#b9c2cc" stroke="#55616f"/>',
                '<rect x="452" y="300" width="70" height="36" fill="#d8dee6" stroke="#55616f"/>',
                _text(486, 292, "真目标", "label", "middle"),
                '<path d="M70 160 C180 180 230 210 325 252" fill="none" class="axis red" marker-end="url(#arrow-warm)"/>',
                '<path d="M80 235 C190 230 285 270 430 352" fill="none" class="axis red" marker-end="url(#arrow-warm)"/>',
                '<path d="M105 102 C230 128 365 190 502 322" fill="none" class="axis red" marker-end="url(#arrow-warm)"/>',
                _text(84, 142, "M1", "small"), _text(92, 224, "M2", "small"), _text(118, 96, "M3", "small"),
                '<path d="M120 390 C220 330 315 286 430 260" fill="none" class="axis blue" marker-end="url(#arrow)"/>',
                '<path d="M160 445 C265 372 350 318 512 248" fill="none" class="thin blue" marker-end="url(#arrow)"/>',
                '<circle cx="300" cy="287" r="34" fill="#d9f3e7" stroke="#087f5b" opacity=".88"/>',
                '<circle cx="375" cy="316" r="45" fill="#d9f3e7" stroke="#087f5b" opacity=".78"/>',
                '<circle cx="440" cy="275" r="38" fill="#d9f3e7" stroke="#087f5b" opacity=".82"/>',
                _text(258, 256, "烟幕云团", "small"),
                _text(260, 456, "遮蔽成立：导弹到真目标的视线穿过有效烟幕", "small", "middle"),
                '<rect x="654" y="92" width="374" height="400" class="note"/>',
                _text(676, 128, "最后答案在量什么", "label"),
                _wrapped_text(676, 160, "5 架无人机、每架最多 3 枚弹，选择航向、速度、投放和起爆时刻，让三枚导弹的有效遮蔽总时间最大。", 22),
                _text(676, 264, "O 奖复现答案", "label"),
                _text(676, 298, "M1 遮蔽 10.3 s", "value"),
                _text(676, 330, "M2 遮蔽 6.2 s", "value"),
                _text(676, 362, "M3 遮蔽 3.4 s", "value"),
                _text(676, 394, "总计 19.9 s", "value"),
            ]
        ),
    )


def _sic() -> str:
    return _base_svg(
        "CUMCM 2025 B 外延层厚度",
        "题面是薄膜多光束干涉；答案是从光谱条纹反推出物理厚度。",
        "\n".join(
            [
                '<rect x="36" y="92" width="580" height="400" class="panel"/>',
                '<rect x="110" y="235" width="410" height="78" fill="#dff4ff" stroke="#244c7c" stroke-width="2"/>',
                '<rect x="110" y="313" width="410" height="92" fill="#efe2cb" stroke="#896b42" stroke-width="2"/>',
                _text(128, 260, "外延层 n1", "label"),
                _text(128, 342, "衬底 n2", "label"),
                '<line x1="164" y1="128" x2="260" y2="235" class="axis warm" marker-end="url(#arrow-warm)"/>',
                '<line x1="260" y1="235" x2="365" y2="128" class="thin blue" marker-end="url(#arrow)"/>',
                '<line x1="260" y1="235" x2="340" y2="313" class="axis warm" marker-end="url(#arrow-warm)"/>',
                '<line x1="340" y1="313" x2="420" y2="235" class="thin green" marker-end="url(#arrow)"/>',
                '<line x1="420" y1="235" x2="520" y2="128" class="thin blue dash" marker-end="url(#arrow)"/>',
                '<line x1="338" y1="235" x2="338" y2="313" stroke="#b42318" stroke-width="2" marker-end="url(#arrow-warm)" marker-start="url(#arrow-warm)"/>',
                _text(350, 278, "厚度 d", "value"),
                _text(163, 118, "入射光", "small"),
                _text(407, 118, "多束反射叠加", "small"),
                '<path d="M86 455 C125 430 164 482 203 455 S281 430 320 455 S398 482 437 455 S515 430 554 455" fill="none" stroke="#087f5b" stroke-width="3"/>',
                _text(320, 482, "光谱条纹周期 -> 反推厚度", "small", "middle"),
                '<rect x="654" y="92" width="374" height="400" class="note"/>',
                _text(676, 128, "最后答案在量什么", "label"),
                _wrapped_text(676, 160, "反射率随波数振荡。条纹周期和多光束修正共同决定外延层厚度；这里的厚度是目标值，不是越大越好。", 22),
                _text(676, 264, "O 奖复现答案", "label"),
                _text(676, 298, "SiC 厚度 8.9815 um", "value"),
                _text(676, 330, "Si 厚度 10.5145 um", "value"),
                _text(676, 374, "方向：目标物理量，越接近推断值越好。", "small"),
            ]
        ),
    )


def _submersible() -> str:
    return _base_svg(
        "MCM 2024 B 潜水器搜索",
        "题面是带漂移的不确定位置搜索；答案是加勒比海迁移时的区域放大系数。",
        "\n".join(
            [
                '<rect x="36" y="92" width="580" height="400" fill="url(#water)" stroke="#7aa8bd"/>',
                '<path d="M65 430 C130 360 190 404 246 342 C322 258 420 320 573 226" fill="none" stroke="#9f8155" stroke-width="22" opacity=".38"/>',
                '<circle cx="235" cy="270" r="5" fill="#b42318"/>',
                _text(250, 265, "最后已知位置", "label"),
                '<ellipse cx="330" cy="290" rx="145" ry="76" transform="rotate(18 330 290)" fill="#fff0df" stroke="#b45b18" opacity=".85"/>',
                '<ellipse cx="360" cy="305" rx="196" ry="103" transform="rotate(18 360 305)" fill="none" stroke="#b42318" stroke-width="3" stroke-dasharray="8 6"/>',
                '<path d="M236 270 C290 272 324 285 360 305" fill="none" class="axis blue" marker-end="url(#arrow)"/>',
                _text(374, 314, "洋流漂移", "small"),
                '<path d="M230 222 L520 315 M220 257 L510 350 M214 292 L500 385 M210 327 L475 405" stroke="#244c7c" stroke-width="3" stroke-linecap="round"/>',
                _text(356, 438, "搜索线覆盖高后验区域；地形复杂处要扩大不确定性", "small", "middle"),
                '<rect x="654" y="92" width="374" height="400" class="note"/>',
                _text(676, 128, "最后答案在量什么", "label"),
                _wrapped_text(676, 160, "把已建搜索模型迁移到加勒比海：洋流更强会拉长漂移椭圆，海底地形更复杂会扩大位置不确定性。", 22),
                _text(676, 264, "O 奖复现答案", "label"),
                _text(676, 298, "洋流不确定性乘数 1.35", "value"),
                _text(676, 330, "地形不确定性乘数 1.20", "value"),
                _text(676, 374, "方向：推荐调整系数，属于目标值。", "small"),
            ]
        ),
    )


def _stair() -> str:
    return _base_svg(
        "MCM 2025 A 楼梯磨损反演",
        "题面是从台阶几何磨损反推历史人流；答案是典型日使用人数和节奏。",
        "\n".join(
            [
                '<rect x="36" y="92" width="580" height="400" class="panel"/>',
                '<path d="M92 422 L198 422 L198 352 L304 352 L304 282 L410 282 L410 212 L540 212" fill="none" stroke="#6f7882" stroke-width="18" stroke-linejoin="round"/>',
                '<path d="M102 417 C145 393 171 393 190 417" fill="none" stroke="#b42318" stroke-width="5"/>',
                '<path d="M208 347 C250 322 280 324 298 347" fill="none" stroke="#b42318" stroke-width="5"/>',
                '<path d="M314 277 C357 252 388 254 404 277" fill="none" stroke="#b42318" stroke-width="5"/>',
                '<path d="M125 170 C150 155 170 155 195 170" fill="none" stroke="#b42318" stroke-width="6"/>',
                '<line x1="125" y1="170" x2="125" y2="238" class="thin red dash"/>',
                '<line x1="195" y1="170" x2="195" y2="238" class="thin red dash"/>',
                '<path d="M125 238 C150 218 170 218 195 238" fill="#fff1f0" stroke="#b42318"/>',
                '<line x1="210" y1="205" x2="284" y2="205" class="axis blue" marker-end="url(#arrow)"/>',
                _text(132, 154, "磨损截面", "label"),
                _text(302, 208, "深度/面积 + 材料 + 年龄", "small"),
                '<rect x="345" y="153" width="190" height="92" fill="#e4f7ef" stroke="#087f5b"/>',
                _text(365, 184, "反演通行次数", "label"),
                _text(365, 216, "再换算成日均人流", "small"),
                _text(316, 466, "几何量不是终点；它被换成“多少人、怎样经过”", "small", "middle"),
                '<rect x="654" y="92" width="374" height="400" class="note"/>',
                _text(676, 128, "最后答案在量什么", "label"),
                _wrapped_text(676, 160, "从磨损形状反推累计使用量，再估计一个典型日约有多少人经过，以及是集中高峰还是全天稀疏。", 22),
                _text(676, 264, "O 奖复现答案", "label"),
                _text(676, 298, "日均使用人数 73.52", "value"),
                _text(676, 330, "短时峰值约 27.6 人", "value"),
                _text(676, 362, "若分散 10 小时：约 4.6 人/小时", "value"),
                _text(676, 406, "方向：历史推断目标值。", "small"),
            ]
        ),
    )


FIGURES: tuple[Figure, ...] = (
    Figure(
        "cumcm-2023-a-heliostat-field",
        "CUMCM 2023 A 定日镜场",
        "CUMCM 2023 A",
        "在定日镜尺寸和安装高度都可以变化时，重新设计镜场，在满足约 60 MW 年平均输出功率的同时，让单位镜面面积输出尽量大。",
        "年平均热功率 60.336111 MW；单位面积功率 0.506192417 kW/m2；光学效率 0.496428083；镜面总面积 119196 m2；定日镜 3311 面。",
        "几何解析 + 太阳运动参数方程 + 镜场约束估计。",
        "看反射光线：镜场不是只求发电多，而是在满足约 60 MW 的同时，让单位面积更有效。",
    ),
    Figure(
        "cumcm-2023-b-multibeam-lines",
        "CUMCM 2023 B 多波束测线",
        "CUMCM 2023 B",
        "给定真实海深数据，设计测线方案，尽量减少测线总长度，同时控制漏测面积和重叠过大的测线长度。",
        "总测线长度 622.0 海里；漏测面积 3.48%；重叠超过 20% 长度 30.0 海里；平均重叠率 10.48%。",
        "海底地形拟合 + 规则化/贪心测线布置。",
        "看条带：测线越少越省，但条带之间不能留下空洞，也不能大量重复扫。",
    ),
    Figure(
        "cumcm-2024-a-dragon-dance",
        "CUMCM 2024 A 板凳龙调头",
        "CUMCM 2024 A",
        "沿着前面求出的调头路径行进时，求龙头最大能跑多快，才能保证所有把手速度都不超过 2 m/s。",
        "龙头最大速度约 2.00002 m/s；龙头 1 m/s 时最大速度比例约 0.99999。",
        "螺线/调头路径参数化 + 刚性把手距离约束 + 速度传播。",
        "看整条链：不是只看龙头，任一把手超速都会让方案不可行。",
    ),
    Figure(
        "cumcm-2025-a-smoke-screen",
        "CUMCM 2025 A 烟幕遮蔽",
        "CUMCM 2025 A",
        "5 架无人机、每架最多 3 枚烟幕弹，同时对 3 枚导弹实施遮蔽，求总体遮蔽时间尽量长的投放方案。",
        "M1 10.3 s；M2 6.2 s；M3 3.4 s；总计 19.9 s。",
        "轨迹几何 + 投放/起爆时序规划优化。",
        "看视线：有效遮蔽就是烟幕云团挡住导弹到真目标的视线。",
    ),
    Figure(
        "cumcm-2025-b-sic-thickness",
        "CUMCM 2025 B 外延层厚度",
        "CUMCM 2025 B",
        "把多光束反射/透射造成的干涉也考虑进去，重新确定碳化硅外延层厚度，并分析结果可靠性。",
        "SiC 厚度 8.9815 um；Si 厚度 10.5145 um。",
        "光谱条纹周期拟合 + 多光束干涉修正。",
        "看薄膜：多束反射叠加形成条纹，条纹周期编码了层厚。",
    ),
    Figure(
        "mcm-2024-b-submersible-search",
        "MCM 2024 B 潜水器搜索",
        "MCM 2024 B",
        "把潜水器搜索模型迁移到加勒比海场景，并说明洋流、海底地形和多潜水器协同时需要怎样调整。",
        "洋流不确定性乘数 1.35；地形不确定性乘数 1.20。",
        "贝叶斯后验位置 + 洋流/地形不确定性放大 + 搜索覆盖规划。",
        "看椭圆：乘数不是目标收益，而是在不同海域下把搜索不确定性放大。",
    ),
    Figure(
        "mcm-2025-a-stair-wear",
        "MCM 2025 A 楼梯磨损反演",
        "MCM 2025 A",
        "根据楼梯磨损反推典型一天大约多少人使用，以及这些人是短时间集中经过还是长时间稀疏经过。",
        "日均使用人数 73.52；短时峰值约 27.6 人；分散到 10 小时则约 4.6 人/小时。",
        "物理磨损反演 + 材料/年龄假设 + 使用模式换算。",
        "看截面：几何磨损被转换成累计通行，再转换成典型日人流。",
    ),
)


SVG_WRITERS = {
    "cumcm-2023-a-heliostat-field": _heliostat,
    "cumcm-2023-b-multibeam-lines": _multibeam,
    "cumcm-2024-a-dragon-dance": _dragon,
    "cumcm-2025-a-smoke-screen": _smoke,
    "cumcm-2025-b-sic-thickness": _sic,
    "mcm-2024-b-submersible-search": _submersible,
    "mcm-2025-a-stair-wear": _stair,
}


def _write_guide() -> None:
    lines = [
        "# Geometry Visual Guide",
        "",
        "This guide adds quick visual intuition for the spatial or geometry-heavy TB-MathModeling tasks. Each figure connects the contest problem geometry to the final numeric answer currently used by the verifier.",
        "",
        "The figures are intentionally schematic: they explain what is being modeled and scored, not the exact coordinates from any one contest attachment.",
        "",
    ]
    for figure in FIGURES:
        rel = f"assets/geometry/{figure.filename}"
        lines.extend(
            [
                f"## {figure.title}",
                "",
                f"![{figure.title}]({rel})",
                "",
                f"- Task: `{figure.slug}`",
                f"- Problem: {figure.final_question}",
                f"- Final verifier answer: {figure.final_answer}",
                f"- Baseline model idea: {figure.baseline_model}",
                f"- Reading hint: {figure.reading_hint}",
                "",
            ]
        )
    GUIDE_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    for slug, writer in SVG_WRITERS.items():
        (ASSET_DIR / f"{slug}.svg").write_text(writer(), encoding="utf-8")
    _write_guide()
    print(f"wrote {GUIDE_PATH}")
    print(f"wrote {len(SVG_WRITERS)} SVG figures under {ASSET_DIR}")


if __name__ == "__main__":
    main()
