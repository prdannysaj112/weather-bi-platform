#!/usr/bin/env python3
from datetime import datetime
from config import OPENWEATHER_API_KEY, DB_PATH
from services.weather_client import OpenWeatherClient
from services.storage import Storage

def main():
    city = "Newark,US"
    client = OpenWeatherClient(OPENWEATHER_API_KEY)
    store = Storage(DB_PATH)

    data = client.fetch_current(city)

    captured_at = datetime.utcnow().isoformat(timespec="seconds") + "Z"
    temp_f = float(data["main"]["temp"])
    humidity = int(data["main"]["humidity"])
    wind_mph = float(data.get("wind", {}).get("speed", 0.0))
    condition = (data.get("weather", [{}])[0].get("main") or "Unknown")

    store.insert_weather(captured_at, city, temp_f, humidity, wind_mph, condition)
    print(f"Inserted weather obs for {city} at {captured_at}: {temp_f}F, {humidity}% humidity")

if __name__ == "__main__":
    main()
