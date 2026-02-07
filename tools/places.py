"""
Places / Attractions tool.
Uses a curated knowledge base of popular destinations + Gemini LLM
to provide top attractions for any city.
"""

from typing import Any, Dict, List
from utils.llm import ask_gemini

# ---------- MCP Tool Schema ----------
TOOL_SCHEMA = {
    "name": "get_attractions",
    "description": "Get top tourist attractions and points of interest for a city.",
    "parameters": {"city": {"type": "string", "description": "City name"}},
    "returns": "list of dicts with name, category, description, rating",
}

# ---------- Curated fallback data ----------
CURATED_ATTRACTIONS: Dict[str, List[Dict[str, Any]]] = {
    "tokyo": [
        {"name": "Senso-ji Temple", "category": "Temple", "description": "Tokyo's oldest and most significant Buddhist temple in Asakusa.", "rating": 4.7},
        {"name": "Shibuya Crossing", "category": "Landmark", "description": "The world's busiest pedestrian crossing, iconic Tokyo experience.", "rating": 4.5},
        {"name": "Meiji Shrine", "category": "Shrine", "description": "Serene Shinto shrine surrounded by a lush forest in central Tokyo.", "rating": 4.8},
        {"name": "Tokyo Skytree", "category": "Observation", "description": "Tallest tower in Japan (634m) with panoramic city views.", "rating": 4.6},
        {"name": "Tsukiji Outer Market", "category": "Food", "description": "World-famous fish market area with incredible street food.", "rating": 4.5},
        {"name": "Akihabara", "category": "Shopping", "description": "Electronics and anime/manga hub, vibrant pop-culture district.", "rating": 4.4},
    ],
    "udaipur": [
        {"name": "City Palace", "category": "Palace", "description": "Majestic palace complex on the banks of Lake Pichola.", "rating": 4.7},
        {"name": "Lake Pichola", "category": "Nature", "description": "Artificial fresh water lake with stunning palace views.", "rating": 4.6},
        {"name": "Jag Mandir", "category": "Palace", "description": "Island palace in Lake Pichola, also known as Lake Garden Palace.", "rating": 4.5},
        {"name": "Saheliyon-ki-Bari", "category": "Garden", "description": "Garden of the Maidens with beautiful fountains and marble art.", "rating": 4.4},
        {"name": "Jagdish Temple", "category": "Temple", "description": "Indo-Aryan temple dedicated to Lord Vishnu, built in 1651.", "rating": 4.5},
        {"name": "Fateh Sagar Lake", "category": "Nature", "description": "Scenic artificial lake surrounded by hills and gardens.", "rating": 4.3},
    ],
    "new york": [
        {"name": "Statue of Liberty", "category": "Monument", "description": "Iconic symbol of freedom on Liberty Island.", "rating": 4.7},
        {"name": "Central Park", "category": "Park", "description": "843-acre urban park, the green heart of Manhattan.", "rating": 4.8},
        {"name": "Times Square", "category": "Landmark", "description": "Brightly lit commercial hub and entertainment center.", "rating": 4.4},
        {"name": "Metropolitan Museum of Art", "category": "Museum", "description": "One of the world's largest and finest art museums.", "rating": 4.8},
        {"name": "Brooklyn Bridge", "category": "Landmark", "description": "Iconic hybrid cable-stayed/suspension bridge, opened 1883.", "rating": 4.7},
        {"name": "Empire State Building", "category": "Observation", "description": "Art Deco skyscraper with observation decks on 86th and 102nd floors.", "rating": 4.6},
    ],
    "london": [
        {"name": "Tower of London", "category": "Castle", "description": "Historic castle and UNESCO site, home to the Crown Jewels.", "rating": 4.7},
        {"name": "British Museum", "category": "Museum", "description": "World-renowned museum of human history and culture.", "rating": 4.8},
        {"name": "Buckingham Palace", "category": "Palace", "description": "Official residence of the British monarch.", "rating": 4.6},
        {"name": "Big Ben & Houses of Parliament", "category": "Landmark", "description": "Iconic clock tower and Gothic Revival Parliament buildings.", "rating": 4.7},
        {"name": "London Eye", "category": "Observation", "description": "135m tall observation wheel on the South Bank of the Thames.", "rating": 4.5},
        {"name": "Hyde Park", "category": "Park", "description": "One of London's largest royal parks, 350 acres of green space.", "rating": 4.6},
    ],
    "paris": [
        {"name": "Eiffel Tower", "category": "Landmark", "description": "Iconic iron lattice tower, symbol of Paris.", "rating": 4.7},
        {"name": "Louvre Museum", "category": "Museum", "description": "World's largest art museum, home to the Mona Lisa.", "rating": 4.8},
        {"name": "Notre-Dame Cathedral", "category": "Cathedral", "description": "Medieval Catholic cathedral, masterpiece of Gothic architecture.", "rating": 4.7},
        {"name": "Champs-Élysées", "category": "Street", "description": "Famous avenue known for luxury shops, cafés, and theatres.", "rating": 4.5},
        {"name": "Sacré-Cœur Basilica", "category": "Church", "description": "White-domed basilica at the summit of Montmartre.", "rating": 4.6},
        {"name": "Musée d'Orsay", "category": "Museum", "description": "Impressionist masterpieces housed in a former railway station.", "rating": 4.7},
    ],
}


def get_attractions(city: str) -> List[Dict[str, Any]]:
    """Get top attractions for a city.

    Uses curated data if available, otherwise asks Gemini to generate a list.

    Args:
        city: City name.

    Returns:
        List of attraction dictionaries.
    """
    city_lower = city.lower().strip()

    # Check curated data first
    if city_lower in CURATED_ATTRACTIONS:
        return CURATED_ATTRACTIONS[city_lower]

    # Try Gemini for other cities
    try:
        prompt = f"""List the top 6 tourist attractions in {city}. 
For each, provide: name, category (e.g., Temple, Museum, Park, Landmark), 
a one-sentence description, and an approximate rating out of 5.
Format as a numbered list like:
1. Name | Category | Description | Rating
"""
        response = ask_gemini(prompt)
        if response.startswith("Error") or response.startswith("LLM Error"):
            raise ValueError(response)

        attractions = []
        for line in response.strip().split("\n"):
            line = line.strip()
            if not line or not line[0].isdigit():
                continue
            # Remove leading number and dot
            line = line.split(".", 1)[-1].strip()
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 3:
                rating = 4.5
                if len(parts) >= 4:
                    try:
                        rating = float(parts[3].replace("/5", "").strip())
                    except (ValueError, IndexError):
                        rating = 4.5
                attractions.append({
                    "name": parts[0],
                    "category": parts[1],
                    "description": parts[2],
                    "rating": rating,
                })
        if attractions:
            return attractions
    except Exception:
        pass

    # Final fallback
    return [
        {"name": f"{city} City Center", "category": "Landmark", "description": f"Explore the vibrant city center of {city}.", "rating": 4.3},
        {"name": f"{city} Historic District", "category": "Heritage", "description": f"Walk through the historical areas of {city}.", "rating": 4.4},
        {"name": f"{city} Local Market", "category": "Market", "description": f"Experience local culture at {city}'s famous markets.", "rating": 4.2},
        {"name": f"{city} Museum", "category": "Museum", "description": f"Discover the art and history of {city}.", "rating": 4.5},
        {"name": f"{city} Park/Garden", "category": "Park", "description": f"Relax in the beautiful green spaces of {city}.", "rating": 4.3},
    ]
