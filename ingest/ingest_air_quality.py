import requests
import json
from datetime import datetime

# Toronto
latitude = 43.65
longitude = -79.35

url = "https://air-quality-api.open-meteo.com/v1/air-quality"

params = {
    "latitude": latitude,
    "longitude": longitude,
    "start_date": "2025-01-01",
    "timezone": "auto",
    "end_date": "2025-12-31",
    "hourly": ["pm10", "pm2_5", "us_aqi"]
}

response = requests.get(url, params=params)

data = response.json()

filename = f"data/bronze/air_quality_{datetime.now().strftime('%Y%m%d')}.json"

with open(filename, "w") as f:
    json.dump(data, f)

print("Air quality data saved to Bronze")