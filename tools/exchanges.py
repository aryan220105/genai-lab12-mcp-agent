"""
Stock Exchange information tool.
Provides exchange names, locations, and Google Maps links.
"""

from typing import Any, Dict, List

# ---------- MCP Tool Schema ----------
TOOL_SCHEMA = {
    "name": "get_exchange_info",
    "description": "Get major stock exchange info for a country including Google Maps links.",
    "parameters": {"country": {"type": "string", "description": "Country name"}},
    "returns": "list of dicts with name, city, maps_link, established, description",
}

# ---------- Exchange Data ----------
EXCHANGES: Dict[str, List[Dict[str, Any]]] = {
    "japan": [
        {
            "name": "Tokyo Stock Exchange (TSE)",
            "city": "Tokyo",
            "lat": 35.6815,
            "lon": 139.7740,
            "maps_link": "https://www.google.com/maps/search/?api=1&query=Tokyo+Stock+Exchange",
            "established": "1878",
            "description": "Third-largest stock exchange in the world by market capitalization.",
            "major_indices": ["Nikkei 225", "TOPIX"],
        },
    ],
    "india": [
        {
            "name": "Bombay Stock Exchange (BSE)",
            "city": "Mumbai",
            "lat": 18.9300,
            "lon": 72.8347,
            "maps_link": "https://www.google.com/maps/search/?api=1&query=Bombay+Stock+Exchange+Mumbai",
            "established": "1875",
            "description": "Asia's oldest stock exchange, located at Dalal Street, Mumbai.",
            "major_indices": ["BSE SENSEX"],
        },
        {
            "name": "National Stock Exchange (NSE)",
            "city": "Mumbai",
            "lat": 19.0544,
            "lon": 72.8407,
            "maps_link": "https://www.google.com/maps/search/?api=1&query=National+Stock+Exchange+Mumbai",
            "established": "1992",
            "description": "India's leading stock exchange by trading volume.",
            "major_indices": ["NIFTY 50"],
        },
    ],
    "united states": [
        {
            "name": "New York Stock Exchange (NYSE)",
            "city": "New York",
            "lat": 40.7069,
            "lon": -74.0113,
            "maps_link": "https://www.google.com/maps/search/?api=1&query=New+York+Stock+Exchange",
            "established": "1792",
            "description": "World's largest stock exchange by market capitalization.",
            "major_indices": ["S&P 500", "Dow Jones"],
        },
        {
            "name": "NASDAQ",
            "city": "New York",
            "lat": 40.7568,
            "lon": -73.9862,
            "maps_link": "https://www.google.com/maps/search/?api=1&query=NASDAQ+MarketSite+Times+Square",
            "established": "1971",
            "description": "Second-largest stock exchange globally, tech-heavy.",
            "major_indices": ["NASDAQ Composite"],
        },
    ],
    "south korea": [
        {
            "name": "Korea Exchange (KRX)",
            "city": "Busan",
            "lat": 35.1028,
            "lon": 129.0322,
            "maps_link": "https://www.google.com/maps/search/?api=1&query=Korea+Exchange+Busan",
            "established": "2005",
            "description": "Sole securities exchange operator in South Korea.",
            "major_indices": ["KOSPI", "KOSDAQ"],
        },
    ],
    "china": [
        {
            "name": "Shanghai Stock Exchange (SSE)",
            "city": "Shanghai",
            "lat": 31.2328,
            "lon": 121.4871,
            "maps_link": "https://www.google.com/maps/search/?api=1&query=Shanghai+Stock+Exchange",
            "established": "1990",
            "description": "Largest stock exchange in China and one of the largest in Asia.",
            "major_indices": ["SSE Composite"],
        },
        {
            "name": "Shenzhen Stock Exchange (SZSE)",
            "city": "Shenzhen",
            "lat": 22.5362,
            "lon": 114.0579,
            "maps_link": "https://www.google.com/maps/search/?api=1&query=Shenzhen+Stock+Exchange",
            "established": "1990",
            "description": "Second stock exchange in mainland China, known for tech listings.",
            "major_indices": ["Shenzhen Composite"],
        },
        {
            "name": "Hong Kong Stock Exchange (HKEX)",
            "city": "Hong Kong",
            "lat": 22.2864,
            "lon": 114.1587,
            "maps_link": "https://www.google.com/maps/search/?api=1&query=Hong+Kong+Stock+Exchange",
            "established": "1891",
            "description": "One of Asia's largest exchanges, gateway for international investors to China.",
            "major_indices": ["Hang Seng Index"],
        },
    ],
    "united kingdom": [
        {
            "name": "London Stock Exchange (LSE)",
            "city": "London",
            "lat": 51.5144,
            "lon": -0.0987,
            "maps_link": "https://www.google.com/maps/search/?api=1&query=London+Stock+Exchange",
            "established": "1801",
            "description": "One of the oldest and largest stock exchanges in Europe.",
            "major_indices": ["FTSE 100", "FTSE 250"],
        },
    ],
}


def get_exchange_info(country: str) -> List[Dict[str, Any]]:
    """Get stock exchange information for a country.

    Args:
        country: Country name.

    Returns:
        List of exchange info dictionaries with Google Maps links.
    """
    country_lower = country.lower().strip()
    exchanges = EXCHANGES.get(country_lower, [])

    if not exchanges:
        # Generate a generic maps link
        return [{
            "name": f"{country} Stock Exchange",
            "city": "Unknown",
            "maps_link": f"https://www.google.com/maps/search/?api=1&query={country.replace(' ', '+')}+Stock+Exchange",
            "established": "N/A",
            "description": f"Stock exchange information for {country} not in database.",
            "major_indices": [],
            "sample": True,
        }]

    return exchanges
