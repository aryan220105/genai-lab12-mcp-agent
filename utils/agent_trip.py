"""
Trip Planner Agent – orchestrates tool calls to build a complete trip plan.
Follows MCP-style: plan tools -> execute -> synthesize via LLM.
Falls back to pre-written content when LLM is unavailable.
"""

from typing import Any, Dict
from utils.trace import MCPTrace
from utils.llm import ask_gemini
from utils.fallbacks import get_fallback_cultural_info, get_fallback_itinerary
from tools.weather import get_current_weather, get_weather_forecast
from tools.flights import search_flights
from tools.hotels import search_hotels
from tools.places import get_attractions


# ---------- MCP Tool Registry ----------
TOOL_REGISTRY = {
    "get_current_weather": get_current_weather,
    "get_weather_forecast": get_weather_forecast,
    "search_flights": search_flights,
    "search_hotels": search_hotels,
    "get_attractions": get_attractions,
}


def _call_tool(trace: MCPTrace, tool_name: str, **kwargs) -> Any:
    """Execute a tool and record it in the MCP trace.

    Args:
        trace: MCPTrace instance for recording.
        tool_name: Name of the tool to call.
        **kwargs: Arguments to pass to the tool.

    Returns:
        The tool's output.
    """
    idx = trace.start_call(tool_name, kwargs)
    try:
        fn = TOOL_REGISTRY[tool_name]
        result = fn(**kwargs)
        trace.end_call(idx, result)
        return result
    except Exception as e:
        trace.end_call(idx, None, error=str(e))
        return {"error": str(e)}


def run_trip_agent(
    from_city: str,
    to_city: str,
    start_date: str,
    end_date: str,
    budget: str = "Medium",
    travelers: int = 2,
    preferences: str = "",
) -> Dict[str, Any]:
    """Run the Trip Planner agent pipeline.

    Steps (MCP-style):
      1. LLM generates cultural/historic paragraph (with fallback)
      2. get_current_weather(to_city)
      3. get_weather_forecast(to_city)
      4. search_flights(from_city, to_city, start_date, travelers)
      5. search_hotels(to_city, start_date, end_date, travelers)
      6. get_attractions(to_city)
      7. LLM generates day-by-day itinerary (with fallback)

    Args:
        from_city: Departure city.
        to_city: Destination city.
        start_date: Trip start date (YYYY-MM-DD).
        end_date: Trip end date (YYYY-MM-DD).
        budget: Budget level (Budget/Medium/Luxury).
        travelers: Number of travelers.
        preferences: User preferences text.

    Returns:
        Dictionary with all sections and the MCP trace.
    """
    trace = MCPTrace()
    results: Dict[str, Any] = {}

    # --- Step 1: Cultural / Historic paragraph via LLM ---
    culture_idx = trace.start_call("llm_cultural_paragraph", {
        "city": to_city,
        "prompt_type": "cultural_historic_info"
    })
    try:
        culture_prompt = f"""Write a concise but rich paragraph (150-200 words) about {to_city} 
covering its cultural significance, historical highlights, and what makes it 
a unique travel destination. Include notable facts, traditions, and atmosphere."""
        culture_text = ask_gemini(culture_prompt)

        if culture_text == "__LLM_UNAVAILABLE__":
            culture_text = get_fallback_cultural_info(to_city)
            trace.end_call(culture_idx, "Used pre-written fallback (LLM unavailable)")
        else:
            trace.end_call(culture_idx, culture_text[:200] + "...")

        results["cultural_info"] = culture_text
    except Exception as e:
        trace.end_call(culture_idx, None, error=str(e))
        results["cultural_info"] = get_fallback_cultural_info(to_city)

    # --- Step 2: Current Weather ---
    results["current_weather"] = _call_tool(trace, "get_current_weather", city=to_city)

    # --- Step 3: Weather Forecast ---
    results["forecast"] = _call_tool(trace, "get_weather_forecast", city=to_city)

    # --- Step 4: Flights ---
    results["flights"] = _call_tool(
        trace, "search_flights",
        from_city=from_city, to_city=to_city,
        date=start_date, travelers=travelers
    )

    # --- Step 5: Hotels ---
    results["hotels"] = _call_tool(
        trace, "search_hotels",
        city=to_city, checkin=start_date,
        checkout=end_date, guests=travelers
    )

    # --- Step 6: Attractions ---
    results["attractions"] = _call_tool(trace, "get_attractions", city=to_city)

    # --- Step 7: Day-by-day Itinerary via LLM ---
    itin_idx = trace.start_call("llm_day_itinerary", {
        "city": to_city,
        "dates": f"{start_date} to {end_date}",
        "prompt_type": "day_by_day_plan"
    })
    try:
        attractions_names = [a.get("name", "") for a in results.get("attractions", []) if isinstance(a, dict)]
        itin_prompt = f"""Create a detailed day-by-day travel itinerary for a trip to {to_city}.

Trip Details:
- From: {from_city}
- Dates: {start_date} to {end_date}
- Travelers: {travelers}
- Budget: {budget}
- Preferences: {preferences if preferences else 'General sightseeing'}

Available Attractions: {', '.join(attractions_names)}

Weather forecast shows: {', '.join([f.get('description', 'N/A') for f in results.get('forecast', [])[:3] if isinstance(f, dict)])}

Format each day as:
**Day N: Title**
- Morning: activity
- Afternoon: activity  
- Evening: activity
- Dining suggestion

Include practical tips for each day. Make it detailed and useful."""
        itinerary_text = ask_gemini(itin_prompt)

        if itinerary_text == "__LLM_UNAVAILABLE__":
            itinerary_text = get_fallback_itinerary(
                to_city, from_city, start_date, end_date,
                travelers, budget, preferences, attractions_names
            )
            trace.end_call(itin_idx, "Used pre-written fallback (LLM unavailable)")
        else:
            trace.end_call(itin_idx, itinerary_text[:200] + "...")

        results["itinerary"] = itinerary_text
    except Exception as e:
        trace.end_call(itin_idx, None, error=str(e))
        attractions_names = [a.get("name", "") for a in results.get("attractions", []) if isinstance(a, dict)]
        results["itinerary"] = get_fallback_itinerary(
            to_city, from_city, start_date, end_date,
            travelers, budget, preferences, attractions_names
        )

    # Attach trace
    results["trace"] = trace

    # Metadata
    results["meta"] = {
        "from_city": from_city,
        "to_city": to_city,
        "start_date": start_date,
        "end_date": end_date,
        "budget": budget,
        "travelers": travelers,
        "preferences": preferences,
    }

    return results
