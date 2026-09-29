"""Scratch: pull 2024 ISO-NE hourly demand, save to parquet, print sanity checks, plot."""
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.data.eia import fetch_raw, parse_demand  # noqa: E402

START, END = "2024-01-01", "2024-12-31"
OUT_PARQUET = ROOT / "data" / "isne_demand.parquet"
YEAR_PLOT = ROOT / "notebooks" / "year_plot.png"
WEEK_PLOT = ROOT / "notebooks" / "week_plot.png"
# Mon-Sun week with no DST change or holiday.
WEEK_START, WEEK_END = "2024-05-06", "2024-05-13"


def main() -> None:
    rows = fetch_raw(START, END)
    print("First 3 raw API rows:")
    for row in rows[:3]:
        print(json.dumps(row, indent=2))

    df = parse_demand(rows)
    OUT_PARQUET.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUT_PARQUET, index=False)
    print(f"\nSaved {OUT_PARQUET}")

    full_range = pd.date_range(f"{START} 00:00", f"{END} 23:00", freq="h", tz="UTC")
    missing = full_range.difference(df["timestamp"])
    print(f"Rows: {len(df)}")
    print(f"Min timestamp: {df['timestamp'].min()}")
    print(f"Max timestamp: {df['timestamp'].max()}")
    print(f"Missing hours: {len(missing)} of {len(full_range)} expected")
    print(f"Null demand values: {df['demand_mw'].isna().sum()}")
    print(df["demand_mw"].describe())

    YEAR_PLOT.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(14, 4))
    ax.plot(df["timestamp"], df["demand_mw"], linewidth=0.5)
    ax.set_title("ISO-NE hourly demand, 2024 (UTC)")
    ax.set_ylabel("Demand (MW)")
    fig.tight_layout()
    fig.savefig(YEAR_PLOT, dpi=120)
    plt.close(fig)

    local = df.assign(timestamp=df["timestamp"].dt.tz_convert("America/New_York"))
    week = local[
        (local["timestamp"] >= pd.Timestamp(WEEK_START, tz="America/New_York"))
        & (local["timestamp"] < pd.Timestamp(WEEK_END, tz="America/New_York"))
    ]
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(week["timestamp"], week["demand_mw"], marker=".", linewidth=1)
    ax.set_title(f"ISO-NE hourly demand, week of {WEEK_START} (America/New_York)")
    ax.set_ylabel("Demand (MW)")
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(WEEK_PLOT, dpi=120)
    plt.close(fig)
    print(f"Saved {YEAR_PLOT} and {WEEK_PLOT}")


if __name__ == "__main__":
    main()
