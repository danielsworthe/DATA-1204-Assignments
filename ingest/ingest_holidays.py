from pathlib import Path
from datetime import datetime
import json

import pandas as pd
import requests

API_BASE = "https://canada-holidays.ca/api/v1"
PROVINCE = "ON"

A3_GOLD_PATH = Path("data/gold/weather_&_air_quality_gold.csv")
BRONZE_DIR = Path("data/bronze")
BRONZE_DIR.mkdir(parents=True, exist_ok=True)


def get_years_from_a3_gold() -> list[int]:
    if A3_GOLD_PATH.exists():
        df = pd.read_csv(A3_GOLD_PATH, usecols=["date"])
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        years = sorted(df["date"].dropna().dt.year.unique().tolist())
        if years:
            return years
    return [datetime.now().year]
print("Gold path conversion successful.")


def fetch_holidays_for_year(year: int) -> dict:
    url = f"{API_BASE}/provinces/{PROVINCE}"
    params = {"year": year, "optional": "false"}
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    return response.json()
print("Fetched holidays successfully.")

def main() -> None:
    years = get_years_from_a3_gold()
    print(f"Fetching holiday data for years: {years}")

    for year in years:
        payload = fetch_holidays_for_year(year)
        out_file = BRONZE_DIR / f"holidays_{PROVINCE}_{year}.json"

        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

        print(f"Saved: {out_file}")


if __name__ == "__main__":
    main()

print("Canadian Holidays API ingestion script successfully ran.")