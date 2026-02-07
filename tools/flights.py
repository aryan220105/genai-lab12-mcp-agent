"""
Flights tool – generates clearly-labeled SAMPLE flight options.
Real flight APIs (Skyscanner, Amadeus) require complex OAuth flows;
this tool provides realistic sample data that satisfies the assignment.
"""

import random
from typing import Any, Dict, List

# ---------- MCP Tool Schema ----------
TOOL_SCHEMA = {
    "name": "search_flights",
    "description": "Search for flight options between two cities on a given date.",
    "parameters": {
        "from_city": {"type": "string", "description": "Departure city"},
        "to_city": {"type": "string", "description": "Arrival city"},
        "date": {"type": "string", "description": "Travel date YYYY-MM-DD"},
        "travelers": {"type": "integer", "description": "Number of travelers"},
    },
    "returns": "list of flight option dicts (airline, departure, arrival, duration, price, stops)",
}

# ---------- Airlines data for realistic samples ----------
AIRLINES = [
    "Air India", "IndiGo", "Emirates", "Singapore Airlines",
    "Japan Airlines", "ANA", "Delta", "United Airlines",
    "British Airways", "Lufthansa", "Qatar Airways", "Thai Airways",
    "Korean Air", "Cathay Pacific", "Turkish Airlines",
]

DURATIONS = ["2h 30m", "3h 15m", "4h 00m", "5h 45m", "7h 20m",
             "8h 10m", "10h 30m", "12h 00m", "14h 25m", "16h 50m"]


def search_flights(from_city: str, to_city: str, date: str, travelers: int = 1) -> List[Dict[str, Any]]:
    """Generate sample flight options between two cities.

    Args:
        from_city: Departure city name.
        to_city: Arrival city name.
        date: Travel date in YYYY-MM-DD format.
        travelers: Number of passengers.

    Returns:
        List of flight option dictionaries. Each is clearly labeled as SAMPLE.
    """
    random.seed(hash(f"{from_city}{to_city}{date}") % (2**31))

    flights = []
    num_options = random.randint(3, 5)

    for i in range(num_options):
        airline = random.choice(AIRLINES)
        dep_hour = random.randint(5, 22)
        dep_min = random.choice([0, 15, 30, 45])
        stops = random.choices([0, 1, 2], weights=[40, 45, 15])[0]
        base_price = random.randint(150, 1200)
        price_per_person = base_price + (stops * random.randint(-50, 100))
        price_per_person = max(100, price_per_person)

        flights.append({
            "airline": airline,
            "flight_no": f"{airline[:2].upper()}{random.randint(100,999)}",
            "from": from_city,
            "to": to_city,
            "date": date,
            "departure": f"{dep_hour:02d}:{dep_min:02d}",
            "duration": random.choice(DURATIONS),
            "stops": stops,
            "stop_label": "Non-stop" if stops == 0 else f"{stops} stop{'s' if stops > 1 else ''}",
            "price_usd": price_per_person,
            "total_usd": price_per_person * travelers,
            "travelers": travelers,
            "class": random.choice(["Economy", "Economy", "Economy", "Premium Economy", "Business"]),
            "sample": True,
            "note": "⚠️ SAMPLE DATA – real flight API not connected",
        })

    # Sort by price
    flights.sort(key=lambda x: x["price_usd"])
    return flights
