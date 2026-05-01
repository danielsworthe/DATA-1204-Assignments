from pathlib import Path
import numpy as np
import pandas as pd

ASSIGNMENT_3_GOLD_PATH = Path("data/gold/weather_&_air_quality_gold.csv")
HOLIDAY_SILVER_PATH = Path("data/silver/holidays.csv")
FINAL_GOLD_PATH = Path("data/gold/final_dataset.csv")
FINAL_GOLD_PATH.parent.mkdir(parents=True, exist_ok=True)

def main() -> None:
    print("Starting Final Gold Dataset creation...")
    
    # 1. Verification of source files
    if not ASSIGNMENT_3_GOLD_PATH.exists():
        raise FileNotFoundError(f"Missing Assignment 3 Gold file: {ASSIGNMENT_3_GOLD_PATH}")
    if not HOLIDAY_SILVER_PATH.exists():
        raise FileNotFoundError(f"Missing holiday Silver file: {HOLIDAY_SILVER_PATH}")

    print("Reading input CSV files...")
    weather = pd.read_csv(ASSIGNMENT_3_GOLD_PATH, parse_dates=["date"])
    holidays = pd.read_csv(HOLIDAY_SILVER_PATH, parse_dates=["date", "holiday_date"])

    # 2. Safety feature checks
    print(f"Checking features in weather data ({len(weather)} rows)...")
    if "bad_air_day" not in weather.columns and "pm25" in weather.columns:
        weather["bad_air_day"] = (weather["pm25"] > 35).astype(int)
        print("Generated missing 'bad_air_day' column.")

    if "bad_weather_day" not in weather.columns and {"precipitation", "temp_max"}.issubset(weather.columns):
        weather["bad_weather_day"] = (
            (weather["precipitation"] > 5) | (weather["temp_max"] < 0)
        ).astype(int)
        print("Generated missing 'bad_weather_day' column.")

    # 3. Merging
    print("Merging weather and holiday data on 'date'...")
    final_df = weather.merge(
        holidays[["date", "holiday_name", "federal_holiday", "province", "is_holiday"]],
        on="date",
        how="left",
    )

    # 4. Fill missing holiday values (The 'Left Join' fallout)
    print("Cleaning up null values for non-holiday rows...")
    final_df["is_holiday"] = final_df["is_holiday"].fillna(0).astype(int)
    final_df["holiday_name"] = final_df["holiday_name"].fillna("No Holiday")
    final_df["federal_holiday"] = final_df["federal_holiday"].fillna(0).astype(int)
    final_df["province"] = final_df["province"].fillna("ON")

    # 5. Feature Engineering
    final_df["day_type"] = np.where(final_df["is_holiday"] == 1, "Holiday", "Non-holiday")

    # Final Validation Print
    holiday_count = final_df["is_holiday"].sum()
    print(f"Merge successful: Found {holiday_count} holiday matches in the dataset.")

    final_df = final_df.sort_values("date")
    final_df.to_csv(FINAL_GOLD_PATH, index=False)

    print("-" * 50)
    print(f"Final Gold dataset saved to: {FINAL_GOLD_PATH}")
    print(f"Total Rows: {len(final_df)}")
    print("-" * 50)

if __name__ == "__main__":
    main()

print("Canadian Holidays API gold level transformation script successfully ran.")