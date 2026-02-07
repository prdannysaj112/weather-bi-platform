from datetime import datetime
from flask import Flask, jsonify, request
from config import OPENWEATHER_API_KEY, DB_PATH
from services.weather_client import OpenWeatherClient
from services.storage import Storage
from services.analytics import simple_sales_forecast

app = Flask(__name__)
client = OpenWeatherClient(OPENWEATHER_API_KEY)
store = Storage(DB_PATH)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ingest/weather")
def ingest_weather():
    """
    POST JSON:
    { "city": "Newark,US" }
    """
    body = request.get_json(silent=True) or {}
    city = body.get("city", "Newark,US")

    data = client.fetch_current(city)
    captured_at = datetime.utcnow().isoformat(timespec="seconds") + "Z"

    temp_f = float(data["main"]["temp"])
    humidity = int(data["main"]["humidity"])
    wind_mph = float(data.get("wind", {}).get("speed", 0.0))
    condition = (data.get("weather", [{}])[0].get("main") or "Unknown")

    store.insert_weather(captured_at, city, temp_f, humidity, wind_mph, condition)
    return jsonify({"inserted": True, "city": city, "captured_at": captured_at})

@app.post("/ingest/sales")
def ingest_sales():
    """
    POST JSON:
    { "date": "2025-06-01", "city": "Newark,US", "sales": 1520.75 }
    """
    body = request.get_json(silent=True) or {}
    date = body.get("date")
    city = body.get("city", "Newark,US")
    sales = body.get("sales")

    if not date or sales is None:
        return jsonify({"error": "date and sales required"}), 400

    store.insert_sales(date, city, float(sales))
    return jsonify({"inserted": True, "date": date, "city": city, "sales": float(sales)})

@app.get("/analytics/summary")
def analytics_summary():
    """
    GET /analytics/summary?city=Newark,US
    """
    city = request.args.get("city", "Newark,US")
    w = store.recent_weather(city, limit=14)
    s = store.recent_sales(city, limit=14)

    forecast = simple_sales_forecast(s)
    return jsonify({
        "city": city,
        "weather_points": len(w),
        "sales_points": len(s),
        "forecast": forecast,
        "recent_weather_sample": w[:5],
        "recent_sales_sample": s[:5],
    })

if __name__ == "__main__":
    app.run(debug=True)
