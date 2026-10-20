# Paper: TB-MathModeling (LaTeX)

LaTeX source for the benchmark paper. `main.tex` includes all sections and
appendices; `refs.bib` is a stub bibliography whose `TODO-*` keys must be
replaced with real citations.

## Build

```sh
pdflatex main && bibtex main && pdflatex main && pdflatex main
# or: latexmk -pdf main.tex   (if latexmk / a TeX distribution is installed)
```

No TeX distribution is installed in this environment, so the source has been
checked structurally (brace/environment balance, cross-reference resolution,
figure-file existence, and every claimed leaderboard number re-derived from the
report) but not compiled here.

## Layout

```
main.tex                     preamble + \input of every section/appendix
refs.bib                     bibliography stub (TODO keys)
sections/
  00-abstract.tex            abstract
  01-intro.tex               motivation, why scoring modeling is hard, contributions
  02-related.tex             related work  [needs citations]
  03-benchmark.tex           METHOD: construction, artifact contract, oracle anchors
  04-scoring.tex             METHOD: direction-aware one-sided scoring, O/B/Robust
  05-verification.tex        METHOD: programmatic gate + Lean certificates + A/B/C
  06-setup.tex               EXPERIMENTS: 16 configs, prompt, environment, protocol
  07-results.tex             RESULTS: main table, multimodal subset, hard-gate effect
  08-analysis.tex            per-task behaviour, pitfalls found/fixed, determinism
  09-case-studies.tex        gpt-5.5 / oracle / deepseek-v4.1 on three problems
  10-limitations.tex         limitations, ethics, reproducibility
  11-conclusion.tex          conclusion
appendix/
  A-dataset.tex              full dataset table, delivered structure, SPLIT = none
  B-environment.tex          host, harbor, docker images, deps, resources, network
  C-settings.tex             per-entry config, command templates, retries, cost
  D-baselines.tex            flash baseline vs outstanding anchor, paper ids
  E-prompts.tex              prompt template + harness wrapping + version caveat
  F-case-studies.tex         full numeric case-study tables
  G-scoring-details.tex      metric panel, formulas, exclusions, hard gates
  H-lean-catalog.tex         624 obligations by task, trust audit, discrimination
figures/                     assets (see below)
```

## Figures included

| file | used in | what it is |
|---|---|---|
| `heliostat_statement_fig1.png` | Sec. 3 (`fig:official-fig`) | an official statement figure, cropped from the source PDF |
| `dragon_statement_fig1.png` | Sec. 9 (`fig:dragon`) | same, for the dragon-dance case study |
| `mm-o-eval-bar.png` | Sec. 9 (`fig:bar`) | multimodal O-Eval board |
| `mm-effect-bar.png`, `mm-robust-bar.png` | (available) | Robust BO-Eval board |
| `mm-o-eval-cost-scatter.png`, `mm-cost.png`, `mm-token-usage.png`, `mm-year-split.png` | (available) | cost / token / year-split charts |

The charts are the published ones from the benchmark site, so they stay
consistent with the numbers in the text. Regenerate them with
`scripts/write_multimodal_board.py` if the leaderboard changes.

## What still needs a human

1. **Citations** — replace the 12 `TODO-*` keys in `sections/02-related.tex`
   and fill `refs.bib` (SWE-bench, Terminal-Bench, GAIA, τ-bench, MATH,
   FrontierMath, miniF2F, NL4Opt, MLE-bench, Lean 4, Mathlib, AlphaProof).
2. **Authors / affiliations** — `main.tex` (`\author{...}`).
3. **Figure selection** — the two "available" chart rows are copied in but not
   yet referenced; add them where useful.
4. **Licence statement** — confirm the redistribution terms for the CUMCM/MCM
   official material (see `sections/10-limitations.tex`).

## Numbers: source of truth

Every quantitative claim in the paper is derived from the generated report
`jobs/terminus2-direction-aware-flash-baseline-bbo-2023-2025.md`. If the board is
regenerated after a scoring change, re-check the tables in
`sections/07-results.tex` and `sections/08-analysis.tex`. The 16 leaderboard rows
were machine-checked against that report when this source was written.

## Facts worth not re-deriving

- 18 tasks (CUMCM 9 + MCM 9), 2023–2025; 21 unique figures across 6 tasks.
- Scoring: `O-Eval = clamp(raw / O_raw, 0, 1)`; `B-Eval = raw − flash_raw`;
  `Robust = clip(gain/gap, ±1)` when `gap ≥ 0.10` else `clip(gain, ±0.10)`; a
  missing artifact scores `−1`. 62 declared metrics, 61 scored.
- Feasibility: programmatic gate 18/18 coverage over six decidable forms;
  Lean layer 624 obligations, `decide`/`omega`, **no Mathlib**, trust audit only
  `[propext, Quot.sound]`, 10/10 discrimination mutations rejected.
- Protocol: one attempt per task; dragon-dance is the only repeated task
  (pass@4, identical to machine precision: mean 1.246266, std 4.6e−16).
