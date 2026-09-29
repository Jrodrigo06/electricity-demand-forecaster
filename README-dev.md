# Developer notes

How to set up, run, and work on this project. The user-facing overview lives in `README.md`.

## Setup

```bash
python -m venv .venv
.venv/Scripts/activate          # Windows (Git Bash); use .venv/bin/activate on macOS/Linux
pip install -r requirements.txt
```

Create `.env` in the repo root (gitignored — note the leading dot):

```
EIA_API_KEY=your_key_here
```

Get a free key at https://www.eia.gov/opendata/register.php.

## Layout

| Path | Purpose |
|---|---|
| `src/data/` | EIA API pull (`eia.py`), cleaning (`clean.py`, stub) |
| `src/features/` | Calendar + weather features (stubs) |
| `src/models/` | Baseline, LightGBM quantile, PyTorch quantile (stubs) |
| `src/eval/` | Pinball loss, coverage, backtest loop (stubs) |
| `src/serving/` | FastAPI app for Cloud Run (stub) |
| `scripts/` | Scratch / one-off scripts |
| `notebooks/` | Exploration and saved plots |
| `tests/` | Mirrors `src/` |
| `data/` | Local data files (gitignored) |

## Common commands

```bash
python scripts/pull_year.py     # pull 2024 ISO-NE demand -> data/isne_demand.parquet + plots in notebooks/
```

## Data notes

- Source: EIA API v2, `electricity/rto/region-data`, respondent `ISNE`, type `D` (demand), `frequency=hourly`.
- `hourly` periods are **UTC** (`"YYYY-MM-DDTHH"`); `value` arrives as a string and is parsed to float.
- `fetch_demand(start, end)`: a date-only `end` is inclusive of the whole day (expanded to hour 23).
- 2024 pull: 8,784 hours, 0 missing timestamps, 3 null values (2024-06-27 05:00, 19:00, 21:00 UTC). Nulls are left as NaN for `clean.py` to handle.

## Gotchas

- **pyarrow is pinned `<24`**: pyarrow 25 breaks parquet I/O with pandas 3.0.x (`ArrowKeyError: No type extension with name arrow.py_extension_type`). Remove the pin once pandas ships a fix.
- The first matplotlib import after a fresh install can take ~2 minutes on Windows while it builds its font cache.
- The `.gitignore` data rule is `/data/` (root only) so it doesn't swallow `src/data/` and `tests/data/`.
