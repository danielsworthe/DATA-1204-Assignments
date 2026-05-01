from pathlib import Path
import glob
import json
import pandas as pd

BRONZE_PATTERN = "data/bronze/holidays_ON_*.json"
SILVER_PATH = Path("data/silver/holidays.csv")
SILVER_PATH.parent.mkdir(parents=True, exist_ok=True)

def main() -> None:
    rows = []

    print(f"Starting transformation. Searching for files matching: {BRONZE_PATTERN}")
    files = sorted(glob.glob(BRONZE_PATTERN))
    
    if not files:
        raise FileNotFoundError(
            f"No holiday JSON files found in Bronze. Expected files like {BRONZE_PATTERN}"
        )

    print(f"Found {len(files)} files to process.")

    for file_name in files:
        print(f"Processing file: {file_name}")
        with open(file_name, "r", encoding="utf-8") as f:
            payload = json.load(f)

        # The Canada Holidays API nests the list under: payload -> province -> holidays
        # We check both levels to ensure the data exists
        province_data = payload.get("province", {})
        holidays = province_data.get("holidays", [])
        
        if not holidays:
            print(f"Warning: No holidays list found in {file_name}. Checking for top-level list...")
            # Fallback in case the API structure changes to top-level
            holidays = payload.get("holidays", [])

        print(f"Extracted {len(holidays)} holiday entries from JSON.")

        for h in holidays:
            rows.append(
                {
                    "holiday_date": h.get("date"),
                    "date": h.get("observedDate", h.get("date")),
                    "holiday_name": h.get("nameEn"),
                    "federal_holiday": int(h.get("federal", 0) or 0),
                    "province": "ON",
                    "is_holiday": 1,
                }
            )

    df = pd.DataFrame(rows)

    if df.empty:
        raise ValueError("No holiday rows were found in the API responses. Verify the JSON structure.")

    print(f"Initial DataFrame created with {len(df)} rows. Cleaning data...")

    # Convert to datetime
    df["holiday_date"] = pd.to_datetime(df["holiday_date"], errors="coerce")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Data cleaning: remove invalid dates and duplicates
    before_count = len(df)
    df = df.dropna(subset=["date"])
    df = df.sort_values("date").drop_duplicates(subset=["date"], keep="first")
    after_count = len(df)

    if before_count != after_count:
        print(f"Removed {before_count - after_count} duplicate or invalid rows.")

    df.to_csv(SILVER_PATH, index=False)
    print(f"Transformation complete. Saved: {SILVER_PATH} ({len(df)} rows)")

if __name__ == "__main__":
    main()

print("Canadian Holidays API transformation script successfully ran.")