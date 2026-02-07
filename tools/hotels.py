"""
Hotels tool – generates clearly-labeled SAMPLE hotel options.
Real hotel APIs (Booking.com, Hotels.com) require RapidAPI keys;
this tool provides realistic sample data that satisfies the assignment.
"""

import random
from typing import Any, Dict, List

# ---------- MCP Tool Schema ----------
TOOL_SCHEMA = {
    "name": "search_hotels",
    "description": "Search for hotel options in a city for given dates.",
    "parameters": {
        "city": {"type": "string", "description": "Destination city"},
        "checkin": {"type": "string", "description": "Check-in date YYYY-MM-DD"},
        "checkout": {"type": "string", "description": "Check-out date YYYY-MM-DD"},
        "guests": {"type": "integer", "description": "Number of guests"},
    },
    "returns": "list of hotel option dicts (name, rating, price_per_night, amenities, location)",
}

# ---------- Hotel name parts for realistic generation ----------
PREFIXES = ["Grand", "Royal", "Imperial", "The", "Hotel", "Park", "Palace", "Heritage"]
SUFFIXES = ["Inn", "Resort", "Suites", "Plaza", "Tower", "Residency", "Hotel", "Lodge"]
AMENITIES_POOL = [
    "Free WiFi", "Pool", "Spa", "Gym", "Restaurant", "Bar",
    "Room Service", "Airport Shuttle", "Parking", "Breakfast Included",
    "Business Center", "Concierge", "Laundry Service", "Ocean View",
]
LOCATIONS = ["City Center", "Near Airport", "Downtown", "Business District",
             "Old Town", "Waterfront", "Cultural Quarter", "Suburban"]


def search_hotels(city: str, checkin: str, checkout: str, guests: int = 2) -> List[Dict[str, Any]]:
    """Generate sample hotel options for a city.

    Args:
        city: Destination city name.
        checkin: Check-in date YYYY-MM-DD.
        checkout: Check-out date YYYY-MM-DD.
        guests: Number of guests.

    Returns:
        List of hotel option dictionaries. Each is clearly labeled as SAMPLE.
    """
    random.seed(hash(f"{city}{checkin}{checkout}") % (2**31))

    hotels = []
    num_options = random.randint(4, 6)

    for i in range(num_options):
        prefix = random.choice(PREFIXES)
        suffix = random.choice(SUFFIXES)
        name = f"{prefix} {city} {suffix}"
        rating = round(random.uniform(3.0, 5.0), 1)
        stars = random.choice([3, 3, 4, 4, 4, 5])
        price = random.randint(40, 350)
        amenities = random.sample(AMENITIES_POOL, k=random.randint(3, 7))

        hotels.append({
            "name": name,
            "stars": stars,
            "rating": rating,
            "review_score": f"{rating}/5.0",
            "price_per_night_usd": price,
            "total_usd": "varies by nights",
            "guests": guests,
            "location": random.choice(LOCATIONS),
            "amenities": amenities,
            "checkin": checkin,
            "checkout": checkout,
            "sample": True,
            "note": "⚠️ SAMPLE DATA – real hotel API not connected",
        })

    # Sort by price
    hotels.sort(key=lambda x: x["price_per_night_usd"])
    return hotels
