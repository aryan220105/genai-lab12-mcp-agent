"""
Stock Indices tool using yfinance.
Fetches current/recent values for major stock market indices.
"""

import yfinance as yf
import streamlit as st
from typing import Any, Dict, List

# ---------- MCP Tool Schema ----------
TOOL_SCHEMA = {
    "name": "get_stock_indices",
    "description": "Get current values of major stock market indices for a country.",
    "parameters": {"country": {"type": "string", "description": "Country name, e.g. 'Japan'"}},
    "returns": "list of dicts with index_name, ticker, value, change, change_pct",
}

# ---------- Country -> Indices mapping ----------
COUNTRY_INDICES: Dict[str, List[Dict[str, str]]] = {
    "japan": [
        {"name": "Nikkei 225", "ticker": "^N225", "exchange": "Tokyo Stock Exchange"},
        {"name": "TOPIX", "ticker": "^TOPX", "exchange": "Tokyo Stock Exchange"},
    ],
    "india": [
        {"name": "BSE SENSEX", "ticker": "^BSESN", "exchange": "Bombay Stock Exchange"},
        {"name": "NIFTY 50", "ticker": "^NSEI", "exchange": "National Stock Exchange"},
    ],
    "united states": [
        {"name": "S&P 500", "ticker": "^GSPC", "exchange": "New York Stock Exchange"},
        {"name": "Dow Jones", "ticker": "^DJI", "exchange": "New York Stock Exchange"},
        {"name": "NASDAQ Composite", "ticker": "^IXIC", "exchange": "NASDAQ"},
    ],
    "south korea": [
        {"name": "KOSPI", "ticker": "^KS11", "exchange": "Korea Exchange"},
        {"name": "KOSDAQ", "ticker": "^KQ11", "exchange": "Korea Exchange"},
    ],
    "china": [
        {"name": "SSE Composite", "ticker": "000001.SS", "exchange": "Shanghai Stock Exchange"},
        {"name": "Shenzhen Composite", "ticker": "399001.SZ", "exchange": "Shenzhen Stock Exchange"},
        {"name": "Hang Seng", "ticker": "^HSI", "exchange": "Hong Kong Stock Exchange"},
    ],
    "united kingdom": [
        {"name": "FTSE 100", "ticker": "^FTSE", "exchange": "London Stock Exchange"},
        {"name": "FTSE 250", "ticker": "^FTMC", "exchange": "London Stock Exchange"},
    ],
}

# ---------- Fallback values ----------
FALLBACK_VALUES = {
    "^N225": 38500.0, "^TOPX": 2700.0,
    "^BSESN": 73500.0, "^NSEI": 22200.0,
    "^GSPC": 5100.0, "^DJI": 39200.0, "^IXIC": 16100.0,
    "^KS11": 2650.0, "^KQ11": 870.0,
    "000001.SS": 3050.0, "399001.SZ": 9500.0, "^HSI": 17200.0,
    "^FTSE": 7700.0, "^FTMC": 19800.0,
}


@st.cache_data(ttl=300)
def get_stock_indices(country: str) -> List[Dict[str, Any]]:
    """Fetch current stock index values for a country.

    Args:
        country: Country name.

    Returns:
        List of index dictionaries with name, ticker, value, change.
    """
    country_lower = country.lower().strip()
    indices_info = COUNTRY_INDICES.get(country_lower, [])

    if not indices_info:
        return [{"error": f"No index data available for {country}", "sample": True}]

    results = []
    for idx_info in indices_info:
        ticker = idx_info["ticker"]
        try:
            tk = yf.Ticker(ticker)
            hist = tk.history(period="5d")

            if hist.empty:
                raise ValueError("No data returned")

            current = round(hist["Close"].iloc[-1], 2)
            if len(hist) >= 2:
                prev = hist["Close"].iloc[-2]
                change = round(current - prev, 2)
                change_pct = round((change / prev) * 100, 2)
            else:
                change = 0.0
                change_pct = 0.0

            results.append({
                "index_name": idx_info["name"],
                "ticker": ticker,
                "exchange": idx_info["exchange"],
                "value": current,
                "change": change,
                "change_pct": change_pct,
                "sample": False,
            })

        except Exception as e:
            fb_val = FALLBACK_VALUES.get(ticker, 0.0)
            results.append({
                "index_name": idx_info["name"],
                "ticker": ticker,
                "exchange": idx_info["exchange"],
                "value": fb_val,
                "change": 0.0,
                "change_pct": 0.0,
                "sample": True,
                "note": f"Fallback data - {str(e)[:50]}",
            })

    return results
