import requests

class OpenWeatherClient:
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def fetch_current(self, city: str) -> dict:
        if not self.api_key:
            raise ValueError("Missing OPENWEATHER_API_KEY (set it in .env).")

        params = {"q": city, "appid": self.api_key, "units": "imperial"}
        r = requests.get(self.BASE_URL, params=params, timeout=10)
        r.raise_for_status()
        return r.json()
