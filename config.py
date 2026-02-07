import os
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
DB_PATH = os.getenv("DB_PATH", "weather_bi.sqlite")
