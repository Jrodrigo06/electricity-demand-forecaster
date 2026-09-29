# CLAUDE.md

Probabilistic day-ahead electricity demand forecasting for the ISO-NE grid (EIA data → features → quantile models → FastAPI on Cloud Run).

See `README-dev.md` for setup, layout, commands, and gotchas.

## Keeping the READMEs up to date

There are two READMEs with different audiences. Every change must leave both accurate.

- **`README.md`** — public/portfolio-facing. Title, one-line description, Status, Problem, Approach, Results. No setup instructions or internal gotchas.
- **`README-dev.md`** — developer-facing. Setup, `.env`, layout, commands, data notes, gotchas, version pins.

Before finishing any task that changes code, data, dependencies, or results, check and update:

1. **New/changed module, script, or command** → `README-dev.md` layout table and "Common commands".
2. **New env var, dependency, or version pin** → `README-dev.md` setup/gotchas (say *why* a pin exists).
3. **Data source or data-quality finding** (gaps, nulls, timezone quirks) → `README-dev.md` "Data notes".
4. **Modeling approach decided or changed** → `README.md` "Approach".
5. **New evaluation numbers** (pinball loss, coverage, backtest) → `README.md` "Results", with the period and setup they came from. Never leave stale numbers.
6. **Milestone reached** → `README.md` "Status".
7. A stub that becomes real code → remove "(stub)" from the `README-dev.md` layout table.

When you report a finished task, state which README sections you updated, or say explicitly that neither needed changes.

## Conventions

- Timestamps are UTC internally (`timestamp` column, tz-aware); convert to `America/New_York` only for display.
- Secrets come from `.env` via python-dotenv. Never hardcode keys; never commit `.env`.
- `tests/` mirrors `src/`.
- Git: do not add `Co-Authored-By` lines to commit messages.
