import requests
import json
from datetime import datetime

# Location: Toronto (for more professional usage)
latitude = 43.65
longitude = -79.35

url = "https://archive-api.open-meteo.com/v1/archive"

params = {
    "latitude": latitude,
    "longitude": longitude,
    "start_date": "2025-01-01",
    "end_date": "2025-12-31",
    "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum"],
    "timezone": "auto"
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    print("Success! Data received.")
else:
    print(f"Error: {response.status_code}")

# Save to Bronze
filename = f"data/bronze/weather_{datetime.now().strftime('%Y%m%d')}.json"

with open(filename, "w") as f:
    json.dump(data, f)

print("Weather data saved to Bronze")