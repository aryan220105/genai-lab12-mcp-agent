"""
Weather tool using OpenWeather API.
Provides current weather and 5-day forecast for any city.
"""

import os
import requests
import streamlit as st
from typing import Any, Dict, List
from datetime import datetime

# ---------- MCP Tool Schemas ----------
CURRENT_WEATHER_SCHEMA = {
    "name": "get_current_weather",
    "description": "Get current weather conditions for a city (temp, humidity, wind, description).",
    "parameters": {"city": {"type": "string", "description": "City name, e.g. 'Tokyo'"}},
    "returns": "dict with temp_c, feels_like_c, description, humidity, wind_kph, icon",
}

FORECAST_SCHEMA = {
    "name": "get_weather_forecast",
    "description": "Get weather forecast for a city for the next 5 days.",
    "parameters": {"city": {"type": "string", "description": "City name"}},
    "returns": "list of dicts with date, temp_min, temp_max, description, humidity",
}

# ---------- Sample / Fallback data ----------
SAMPLE_CURRENT = {
    "temp_c": 22,
    "feels_like_c": 21,
    "description": "Partly cloudy",
    "humidity": 55,
    "wind_kph": 12.5,
    "icon": "02d",
    "sample": True,
}

SAMPLE_FORECAST = [
    {"date": "Day 1", "temp_min": 18, "temp_max": 25, "description": "Sunny", "humidity": 50},
    {"date": "Day 2", "temp_min": 17, "temp_max": 24, "description": "Partly cloudy", "humidity": 55},
    {"date": "Day 3", "temp_min": 19, "temp_max": 26, "description": "Clear sky", "humidity": 48},
    {"date": "Day 4", "temp_min": 16, "temp_max": 23, "description": "Light rain", "humidity": 70},
    {"date": "Day 5", "temp_min": 18, "temp_max": 24, "description": "Sunny", "humidity": 52},
]


# ---------- Tool Functions ----------
@st.cache_data(ttl=600)
def get_current_weather(city: str) -> Dict[str, Any]:
    """Fetch current weather for a city.

    Args:
        city: Name of the city.

    Returns:
        Dictionary with temperature, description, humidity, wind speed.
    """
    api_key = os.getenv("OPENWEATHER_API_KEY", "")
    if not api_key:
        return {**SAMPLE_CURRENT, "city": city, "note": "SAMPLE DATA - OPENWEATHER_API_KEY not set"}

    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {"q": city, "appid": api_key, "units": "metric"}
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        return {
            "city": city,
            "temp_c": round(data["main"]["temp"], 1),
            "feels_like_c": round(data["main"]["feels_like"], 1),
            "description": data["weather"][0]["description"].title(),
            "humidity": data["main"]["humidity"],
            "wind_kph": round(data["wind"]["speed"] * 3.6, 1),
            "icon": data["weather"][0]["icon"],
            "sample": False,
        }
    except Exception as e:
        return {**SAMPLE_CURRENT, "city": city, "note": f"SAMPLE DATA - API error: {e}"}


@st.cache_data(ttl=600)
def get_weather_forecast(city: str) -> List[Dict[str, Any]]:
    """Fetch 5-day weather forecast for a city.

    Args:
        city: Name of the city.

    Returns:
        List of daily forecast dictionaries.
    """
    api_key = os.getenv("OPENWEATHER_API_KEY", "")
    if not api_key:
        return [{"sample": True, "note": "SAMPLE DATA", **f} for f in SAMPLE_FORECAST]

    try:
        url = "https://api.openweathermap.org/data/2.5/forecast"
        params = {"q": city, "appid": api_key, "units": "metric"}
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        # Aggregate by day (API gives 3-hour intervals)
        daily: Dict[str, Dict] = {}
        for item in data["list"]:
            date_str = item["dt_txt"].split(" ")[0]
            if date_str not in daily:
                daily[date_str] = {
                    "date": date_str,
                    "temps": [],
                    "descriptions": [],
                    "humidities": [],
                }
            daily[date_str]["temps"].append(item["main"]["temp"])
            daily[date_str]["descriptions"].append(item["weather"][0]["description"])
            daily[date_str]["humidities"].append(item["main"]["humidity"])

        forecast = []
        for date_str, d in list(daily.items())[:5]:
            forecast.append({
                "date": date_str,
                "temp_min": round(min(d["temps"]), 1),
                "temp_max": round(max(d["temps"]), 1),
                "description": max(set(d["descriptions"]), key=d["descriptions"].count).title(),
                "humidity": round(sum(d["humidities"]) / len(d["humidities"])),
                "sample": False,
            })
        return forecast

    except Exception as e:
        return [{"sample": True, "note": f"SAMPLE DATA - API error: {e}", **f} for f in SAMPLE_FORECAST]
