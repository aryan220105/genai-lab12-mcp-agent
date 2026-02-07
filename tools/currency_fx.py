"""
Currency & FX Rates tool.
- Official currency info from REST Countries API.
- FX conversion rates from ExchangeRate-API.
"""

import os
import requests
import streamlit as st
from typing import Any, Dict, Optional

# ---------- MCP Tool Schemas ----------
CURRENCY_INFO_SCHEMA = {
    "name": "get_currency_info",
    "description": "Get official currency name and code for a country using REST Countries API.",
    "parameters": {"country": {"type": "string", "description": "Country name, e.g. 'Japan'"}},
    "returns": "dict with currency_code, currency_name, currency_symbol, country",
}

FX_RATES_SCHEMA = {
    "name": "get_fx_rates",
    "description": "Get exchange rates for a currency vs USD, INR, GBP, EUR.",
    "parameters": {"currency_code": {"type": "string", "description": "ISO currency code, e.g. 'JPY'"}},
    "returns": "dict with base, rates (USD, INR, GBP, EUR), last_updated",
}

# ---------- Fallback data ----------
FALLBACK_CURRENCIES = {
    "japan": {"currency_code": "JPY", "currency_name": "Japanese yen", "currency_symbol": "¥", "capital": "Tokyo", "latlng": [36.0, 138.0]},
    "india": {"currency_code": "INR", "currency_name": "Indian rupee", "currency_symbol": "₹", "capital": "New Delhi", "latlng": [20.0, 77.0]},
    "united states": {"currency_code": "USD", "currency_name": "United States dollar", "currency_symbol": "$", "capital": "Washington, D.C.", "latlng": [38.0, -97.0]},
    "south korea": {"currency_code": "KRW", "currency_name": "South Korean won", "currency_symbol": "₩", "capital": "Seoul", "latlng": [37.0, 127.5]},
    "china": {"currency_code": "CNY", "currency_name": "Chinese yuan", "currency_symbol": "¥", "capital": "Beijing", "latlng": [35.0, 105.0]},
    "united kingdom": {"currency_code": "GBP", "currency_name": "British pound sterling", "currency_symbol": "£", "capital": "London", "latlng": [54.0, -2.0]},
}

FALLBACK_RATES = {
    "JPY": {"USD": 0.0067, "INR": 0.56, "GBP": 0.0053, "EUR": 0.0062},
    "INR": {"USD": 0.012, "INR": 1.0, "GBP": 0.0095, "EUR": 0.011},
    "USD": {"USD": 1.0, "INR": 83.5, "GBP": 0.79, "EUR": 0.92},
    "KRW": {"USD": 0.00075, "INR": 0.063, "GBP": 0.00059, "EUR": 0.00069},
    "CNY": {"USD": 0.14, "INR": 11.5, "GBP": 0.11, "EUR": 0.13},
    "GBP": {"USD": 1.27, "INR": 105.8, "GBP": 1.0, "EUR": 1.17},
}


@st.cache_data(ttl=3600)
def get_currency_info(country: str) -> Dict[str, Any]:
    """Get official currency information for a country.

    Args:
        country: Country name (e.g., 'Japan', 'India').

    Returns:
        Dictionary with currency code, name, symbol, capital, and coordinates.
    """
    country_lower = country.lower().strip()

    try:
        url = f"https://restcountries.com/v3.1/name/{country}"
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        if data and len(data) > 0:
            c = data[0]
            currencies = c.get("currencies", {})
            if currencies:
                code = list(currencies.keys())[0]
                cur = currencies[code]
                return {
                    "country": c.get("name", {}).get("common", country),
                    "currency_code": code,
                    "currency_name": cur.get("name", "Unknown"),
                    "currency_symbol": cur.get("symbol", ""),
                    "capital": c.get("capital", ["Unknown"])[0] if c.get("capital") else "Unknown",
                    "latlng": c.get("latlng", [0, 0]),
                    "flag": c.get("flag", ""),
                    "sample": False,
                }
    except Exception as e:
        pass

    # Fallback
    if country_lower in FALLBACK_CURRENCIES:
        fb = FALLBACK_CURRENCIES[country_lower]
        return {
            "country": country,
            **fb,
            "flag": "",
            "sample": True,
            "note": "Fallback data used",
        }

    return {
        "country": country,
        "currency_code": "N/A",
        "currency_name": "Unknown",
        "currency_symbol": "",
        "capital": "Unknown",
        "latlng": [0, 0],
        "flag": "",
        "sample": True,
        "note": "Country not found",
    }


@st.cache_data(ttl=3600)
def get_fx_rates(currency_code: str) -> Dict[str, Any]:
    """Get exchange rates for a currency against USD, INR, GBP, EUR.

    Args:
        currency_code: ISO 4217 currency code (e.g., 'JPY').

    Returns:
        Dictionary with conversion rates.
    """
    api_key = os.getenv("EXCHANGERATE_API_KEY", "")
    target_currencies = ["USD", "INR", "GBP", "EUR"]

    if not api_key:
        if currency_code in FALLBACK_RATES:
            return {
                "base": currency_code,
                "rates": FALLBACK_RATES[currency_code],
                "last_updated": "N/A",
                "sample": True,
                "note": "SAMPLE DATA - EXCHANGERATE_API_KEY not set",
            }
        return {
            "base": currency_code,
            "rates": {c: 0.0 for c in target_currencies},
            "last_updated": "N/A",
            "sample": True,
            "note": "Currency not found in fallback data",
        }

    try:
        url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{currency_code}"
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        if data.get("result") == "success":
            all_rates = data.get("conversion_rates", {})
            rates = {}
            for tc in target_currencies:
                rates[tc] = all_rates.get(tc, 0.0)
            return {
                "base": currency_code,
                "rates": rates,
                "last_updated": data.get("time_last_update_utc", "Unknown"),
                "sample": False,
            }
    except Exception as e:
        pass

    # Fallback
    if currency_code in FALLBACK_RATES:
        return {
            "base": currency_code,
            "rates": FALLBACK_RATES[currency_code],
            "last_updated": "N/A",
            "sample": True,
            "note": "Fallback data - API error",
        }

    return {
        "base": currency_code,
        "rates": {c: 0.0 for c in target_currencies},
        "last_updated": "N/A",
        "sample": True,
        "note": "Currency not found",
    }
