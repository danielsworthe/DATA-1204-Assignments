import json
import pandas as pd
import glob

# Grab the latest air quality file from the bronze folder
file = sorted(glob.glob("data/bronze/air_quality_*.json"))[-1]

with open(file) as f:
    data = json.load(f)

# 1. Extract the new variables from the JSON structure
df = pd.DataFrame({
    "datetime": data["hourly"]["time"],
    "pm25": data["hourly"]["pm2_5"],
    "pm10": data["hourly"]["pm10"],
    "us_aqi": data["hourly"]["us_aqi"]
})

# Convert string to datetime objects
df["datetime"] = pd.to_datetime(df["datetime"])
df["date"] = df["datetime"].dt.date

# 2. Convert hourly → daily average for ALL numeric variables
# We use a list [["pm25", "pm10", "us_aqi"]] to calculate all means at once
df_daily = df.groupby("date")[["pm25", "pm10", "us_aqi"]].mean().reset_index()

# 3. Rounds all values to 2 decimal places for cleanness 
df_daily = df_daily.round(2)

# 4. Save the enriched dataset to Silver
df_daily.to_csv("data/silver/air_quality.csv", index=False)

print(f"Success: Processed {file}")
print("Daily averages for PM2.5, PM10, and US AQI saved to Silver.")