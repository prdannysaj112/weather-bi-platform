# weather-bi-platform

# Weather-Based Business Intelligence Platform

A backend project that ingests weather data via a third-party API, stores observations and business sales signals, and exposes analytics endpoints for basic forecasting and reporting.

## Features
- Ingest weather observations (OpenWeather API) with validation + structured storage
- Store sales signals and correlate with weather (baseline forecast method)
- REST API endpoints for ingestion and analytics summaries

## Tech
- Python, Flask
- SQLite for storage
- Requests + dotenv
