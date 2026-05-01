import pandas as pd

weather = pd.read_csv("data/silver/weather.csv")
air = pd.read_csv("data/silver/air_quality.csv")

# Making both date columns into datetime objects to setup proper merge 
weather["date"] = pd.to_datetime(weather["date"])
air["date"] = pd.to_datetime(air["date"])

# Merge on date
df = pd.merge(weather, air, on="date", how="inner")

# Features
df["bad_weather_day"] = (df["precipitation"] > 5) | (df["temp_max"] < 0)
df["bad_air_day"] = df["pm25"] > 35

# Rounding certain columns to standard place values
df = df.round({"pm25": 2, "pm10": 2, "us_aqi": 0}) # AQI is usually a whole number

# Save
df.to_csv("data/gold/weather_&_air_quality_gold.csv", index=False)

print("Gold dataset created")