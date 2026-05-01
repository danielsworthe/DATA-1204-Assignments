import json
import pandas as pd
import glob

# Get latest Bronze file
file = sorted(glob.glob("data/bronze/weather_*.json"))[-1]

with open(file) as f:
    data = json.load(f)

df = pd.DataFrame({
    "date": data["daily"]["time"],
    "temp_max": data["daily"]["temperature_2m_max"],
    "temp_min": data["daily"]["temperature_2m_min"],
    "precipitation": data["daily"]["precipitation_sum"]
})

df.to_csv("data/silver/weather.csv", index=False)

print("Weather data saved to Silver")