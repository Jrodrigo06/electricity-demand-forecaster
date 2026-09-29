"""Pull hourly ISO-NE demand data from the EIA API (v2, RTO region data)."""
import os

import pandas as pd
import requests
from dotenv import load_dotenv

BASE_URL = "https://api.eia.gov/v2/electricity/rto/region-data/data/"
PAGE_SIZE = 5000


def _api_key() -> str:
    load_dotenv()
    key = os.getenv("EIA_API_KEY")
    if not key:
        raise RuntimeError("EIA_API_KEY is not set (add it to .env or the environment).")
    return key


def _to_period(value: str, end_of_day: bool) -> str:
    """Convert a date/datetime string to EIA's hourly period format 'YYYY-MM-DDTHH' (UTC).

    A bare date ('2024-12-31') is expanded to hour 00 for start, hour 23 for end,
    so the end date is inclusive of the whole day.
    """
    ts = pd.Timestamp(value)
    if end_of_day and len(value) == 10:
        ts = ts + pd.Timedelta(hours=23)
    return ts.strftime("%Y-%m-%dT%H")


def fetch_raw(start: str, end: str, respondent: str = "ISNE") -> list[dict]:
    """Fetch all raw hourly demand records from the EIA API, paging by offset."""
    params = {
        "api_key": _api_key(),
        "frequency": "hourly",
        "data[0]": "value",
        "facets[respondent][]": respondent,
        "facets[type][]": "D",
        "start": _to_period(start, end_of_day=False),
        "end": _to_period(end, end_of_day=True),
        "sort[0][column]": "period",
        "sort[0][direction]": "asc",
        "length": PAGE_SIZE,
    }

    rows: list[dict] = []
    offset = 0
    while True:
        resp = requests.get(BASE_URL, params={**params, "offset": offset}, timeout=60)
        resp.raise_for_status()
        body = resp.json()["response"]
        page = body["data"]
        rows.extend(page)
        total = int(body["total"])
        offset += len(page)
        if not page or offset >= total:
            break
    return rows


def parse_demand(rows: list[dict]) -> pd.DataFrame:
    """Convert raw EIA records to a DataFrame with columns timestamp (UTC), demand_mw (float)."""
    if not rows:
        return pd.DataFrame(
            {"timestamp": pd.Series(dtype="datetime64[ns, UTC]"), "demand_mw": pd.Series(dtype=float)}
        )
    raw = pd.DataFrame(rows)
    df = pd.DataFrame(
        {
            "timestamp": pd.to_datetime(raw["period"], format="%Y-%m-%dT%H", utc=True),
            "demand_mw": pd.to_numeric(raw["value"], errors="coerce").astype(float),
        }
    )
    return df.sort_values("timestamp").reset_index(drop=True)


def fetch_demand(start: str, end: str, respondent: str = "ISNE") -> pd.DataFrame:
    """Fetch hourly demand for a respondent between start and end (inclusive, UTC)."""
    return parse_demand(fetch_raw(start, end, respondent))
