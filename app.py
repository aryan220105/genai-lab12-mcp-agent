"""
GenAI Lab 12 – Travel & Market Intelligence Agent
A Streamlit app with two tabs:
  Tab 1: Trip Planner Agent (weather, flights, hotels, attractions, itinerary)
  Tab 2: Currency & Stock Market Agent (currency, FX, indices, exchange maps)

Uses MCP-style tool orchestration with Gemini LLM.
"""

import os
import streamlit as st
import pandas as pd
from datetime import date, timedelta
from dotenv import load_dotenv

# Load .env file if present
load_dotenv()

# --- Page Config ---
st.set_page_config(
    page_title="GenAI Lab 12 – Travel & Market Agent",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ====================================================================
# SIDEBAR – API Key Status & Info
# ====================================================================
with st.sidebar:
    st.header("🔑 API Key Status")
    st.caption("Keys are read from environment variables or .env file")

    keys_config = {
        "GROQ_API_KEY": "Groq LLM (primary)",
        "GOOGLE_API_KEY": "Gemini LLM (fallback)",
        "OPENWEATHER_API_KEY": "Weather data",
        "EXCHANGERATE_API_KEY": "FX rates",
    }

    all_ok = True
    for key_name, desc in keys_config.items():
        val = os.getenv(key_name, "")
        if val:
            st.markdown(f"✅ **{key_name}** – {desc}")
        else:
            st.markdown(f"❌ **{key_name}** – {desc}")
            all_ok = False

    if all_ok:
        st.success("All required keys are set!")
    else:
        st.warning("Some keys are missing. Features using those APIs will show sample/fallback data.")

    st.divider()
    st.markdown("### ℹ️ About")
    st.markdown("""
    **GenAI Lab 12** – MCP-style Travel & Market Agent  
    Built with Streamlit + Groq/Gemini + LangChain-style tools  
    
    **Tools used:**
    - Groq LLM / Gemini (AI reasoning)
    - OpenWeather API (weather)
    - Sample generator (flights & hotels)
    - REST Countries API (currency)
    - ExchangeRate API (FX rates)
    - yfinance (stock indices)
    - Google Maps (exchange locations)
    """)

# ====================================================================
# MAIN APP
# ====================================================================
st.title("🌍 GenAI Travel & Market Intelligence Agent")
st.caption("MCP-style multi-tool agent powered by Gemini LLM")

tab1, tab2 = st.tabs(["🗺️ Trip Planner", "💱 Currency & Stocks"])


# ====================================================================
# TAB 1 – TRIP PLANNER
# ====================================================================
with tab1:
    st.header("🗺️ Trip Planner Agent")
    st.markdown("Plan your perfect trip with AI-powered insights, real-time weather, and curated recommendations.")

    # --- Input Form ---
    col1, col2 = st.columns(2)
    with col1:
        from_city = st.text_input("🛫 From City", value="New Delhi", key="trip_from")
        start_date = st.date_input("📅 Start Date", value=date.today() + timedelta(days=7), key="trip_start")
        budget = st.selectbox("💰 Budget", ["Budget", "Medium", "Luxury"], index=1, key="trip_budget")
    with col2:
        to_city = st.text_input("🛬 To City", value="Tokyo", key="trip_to")
        end_date = st.date_input("📅 End Date", value=date.today() + timedelta(days=12), key="trip_end")
        travelers = st.number_input("👥 Travelers", min_value=1, max_value=10, value=2, key="trip_travelers")

    preferences = st.text_area(
        "🎯 Preferences & Interests",
        placeholder="e.g., temples, street food, nightlife, museums, adventure, shopping...",
        key="trip_prefs",
    )

    plan_btn = st.button("✈️ Plan My Trip", type="primary", use_container_width=True, key="plan_trip")

    if plan_btn:
        if not from_city or not to_city:
            st.error("Please enter both departure and destination cities.")
        elif start_date >= end_date:
            st.error("End date must be after start date.")
        else:
            with st.spinner("🤖 Agent is planning your trip... calling tools & consulting Gemini..."):
                from utils.agent_trip import run_trip_agent

                results = run_trip_agent(
                    from_city=from_city,
                    to_city=to_city,
                    start_date=str(start_date),
                    end_date=str(end_date),
                    budget=budget,
                    travelers=travelers,
                    preferences=preferences,
                )

            # --- Display Results ---
            st.divider()
            st.subheader(f"📍 Trip Plan: {from_city} → {to_city}")
            st.caption(f"{start_date} to {end_date} | {travelers} traveler(s) | {budget} budget")

            # --- Cultural / Historic Info ---
            with st.expander("🏛️ Cultural & Historic Overview", expanded=True):
                st.markdown(results.get("cultural_info", "N/A"))

            # --- Current Weather ---
            with st.expander("🌤️ Current Weather", expanded=True):
                weather = results.get("current_weather", {})
                if isinstance(weather, dict):
                    if weather.get("sample"):
                        st.info(f"⚠️ {weather.get('note', 'Sample data')}")
                    wcol1, wcol2, wcol3, wcol4 = st.columns(4)
                    wcol1.metric("🌡️ Temperature", f"{weather.get('temp_c', 'N/A')}°C")
                    wcol2.metric("💧 Humidity", f"{weather.get('humidity', 'N/A')}%")
                    wcol3.metric("💨 Wind", f"{weather.get('wind_kph', 'N/A')} km/h")
                    wcol4.metric("🌤️ Condition", weather.get("description", "N/A"))

            # --- Weather Forecast ---
            with st.expander("📊 Weather Forecast (Trip Dates)", expanded=True):
                forecast = results.get("forecast", [])
                if forecast and isinstance(forecast, list):
                    if forecast[0].get("sample"):
                        st.info("⚠️ Sample forecast data shown")
                    df_forecast = pd.DataFrame([
                        {
                            "Date": f.get("date", "N/A"),
                            "Min °C": f.get("temp_min", "N/A"),
                            "Max °C": f.get("temp_max", "N/A"),
                            "Condition": f.get("description", "N/A"),
                            "Humidity %": f.get("humidity", "N/A"),
                        }
                        for f in forecast
                    ])
                    st.dataframe(df_forecast, use_container_width=True, hide_index=True)

            # --- Flights ---
            with st.expander("✈️ Flight Options", expanded=True):
                flights = results.get("flights", [])
                if flights and isinstance(flights, list):
                    if flights[0].get("sample"):
                        st.info("⚠️ SAMPLE flight data – real flight API not connected")
                    df_flights = pd.DataFrame([
                        {
                            "Airline": f.get("airline", "N/A"),
                            "Flight": f.get("flight_no", "N/A"),
                            "Departure": f.get("departure", "N/A"),
                            "Duration": f.get("duration", "N/A"),
                            "Stops": f.get("stop_label", "N/A"),
                            "Class": f.get("class", "N/A"),
                            "Price/Person (USD)": f"${f.get('price_usd', 0):,}",
                            "Total (USD)": f"${f.get('total_usd', 0):,}",
                        }
                        for f in flights
                    ])
                    st.dataframe(df_flights, use_container_width=True, hide_index=True)

            # --- Hotels ---
            with st.expander("🏨 Hotel Options", expanded=True):
                hotels = results.get("hotels", [])
                if hotels and isinstance(hotels, list):
                    if hotels[0].get("sample"):
                        st.info("⚠️ SAMPLE hotel data – real hotel API not connected")
                    df_hotels = pd.DataFrame([
                        {
                            "Hotel": h.get("name", "N/A"),
                            "Stars": "⭐" * h.get("stars", 3),
                            "Rating": h.get("review_score", "N/A"),
                            "Location": h.get("location", "N/A"),
                            "Price/Night (USD)": f"${h.get('price_per_night_usd', 0):,}",
                            "Amenities": ", ".join(h.get("amenities", [])),
                        }
                        for h in hotels
                    ])
                    st.dataframe(df_hotels, use_container_width=True, hide_index=True)

            # --- Attractions ---
            with st.expander("🎯 Top Attractions & Places", expanded=True):
                attractions = results.get("attractions", [])
                if attractions and isinstance(attractions, list):
                    for att in attractions:
                        if isinstance(att, dict):
                            st.markdown(
                                f"**{att.get('name', 'N/A')}** ({att.get('category', '')}) "
                                f"– ⭐ {att.get('rating', 'N/A')}"
                            )
                            st.caption(att.get("description", ""))

            # --- Day-by-Day Itinerary ---
            with st.expander("📋 Day-by-Day Itinerary", expanded=True):
                st.markdown(results.get("itinerary", "N/A"))

            # --- MCP Trace Panel ---
            with st.expander("🔧 MCP Agent Trace (Tool Calls)", expanded=False):
                trace = results.get("trace")
                if trace:
                    st.markdown("**Tool Execution Log:**")
                    for i, call in enumerate(trace.get_calls()):
                        status_icon = "✅" if call.status == "success" else "❌"
                        st.markdown(f"""
**{i+1}. {status_icon} `{call.tool_name}`**  
- **Inputs:** `{call.inputs}`  
- **Status:** {call.status} | **Duration:** {call.duration_ms}ms  
- **Output preview:** `{str(call.output)[:200]}{'...' if call.output and len(str(call.output)) > 200 else ''}`  
{f'- **Error:** {call.error}' if call.error else ''}
---""")
                    st.info(f"Total tool calls: {len(trace.get_calls())}")


# ====================================================================
# TAB 2 – CURRENCY & STOCKS
# ====================================================================
with tab2:
    st.header("💱 Currency & Stock Market Agent")
    st.markdown("Get real-time currency info, exchange rates, stock indices, and exchange locations.")

    # --- Input Form ---
    col1, col2 = st.columns([1, 2])
    with col1:
        country_options = ["Japan", "India", "United States", "South Korea", "China", "United Kingdom"]
        selected_country = st.selectbox("🌐 Select Country", country_options, key="market_country")
    with col2:
        extra_query = st.text_input(
            "💬 Additional Query (optional)",
            placeholder="e.g., How is the tech sector performing?",
            key="market_query",
        )

    market_btn = st.button("📊 Get Market Info", type="primary", use_container_width=True, key="get_market")

    if market_btn:
        with st.spinner("🤖 Agent is fetching market data... calling tools & consulting Gemini..."):
            from utils.agent_market import run_market_agent

            results = run_market_agent(
                country=selected_country,
                extra_query=extra_query,
            )

        # --- Display Results ---
        st.divider()
        st.subheader(f"📊 Market Intelligence: {selected_country}")

        # --- Currency Info ---
        with st.expander("💵 Official Currency", expanded=True):
            cur_info = results.get("currency_info", {})
            if isinstance(cur_info, dict):
                ccol1, ccol2, ccol3 = st.columns(3)
                ccol1.metric("Currency", cur_info.get("currency_name", "N/A"))
                ccol2.metric("Code", cur_info.get("currency_code", "N/A"))
                ccol3.metric("Symbol", cur_info.get("currency_symbol", "N/A"))
                if cur_info.get("flag"):
                    st.caption(f"Flag: {cur_info['flag']}  |  Capital: {cur_info.get('capital', 'N/A')}")

        # --- FX Rates ---
        with st.expander("💱 Exchange Rates", expanded=True):
            fx_data = results.get("fx_rates", {})
            if isinstance(fx_data, dict):
                if fx_data.get("sample"):
                    st.info(f"⚠️ {fx_data.get('note', 'Sample data')}")
                base = fx_data.get("base", "N/A")
                rates = fx_data.get("rates", {})
                if rates:
                    st.markdown(f"**Base: 1 {base}**")
                    df_rates = pd.DataFrame([
                        {"Target Currency": tc, "Rate": f"{rate:.6f}" if rate < 1 else f"{rate:.4f}"}
                        for tc, rate in rates.items()
                    ])
                    st.dataframe(df_rates, use_container_width=True, hide_index=True)
                    st.caption(f"Last updated: {fx_data.get('last_updated', 'N/A')}")

        # --- Stock Exchanges ---
        with st.expander("🏦 Stock Exchanges", expanded=True):
            exchanges = results.get("exchanges", [])
            if exchanges and isinstance(exchanges, list):
                for ex in exchanges:
                    if isinstance(ex, dict):
                        st.markdown(f"### {ex.get('name', 'N/A')}")
                        st.markdown(f"📍 **City:** {ex.get('city', 'N/A')}  |  "
                                    f"📅 **Established:** {ex.get('established', 'N/A')}")
                        st.markdown(f"{ex.get('description', '')}")
                        if ex.get("major_indices"):
                            st.markdown(f"**Major Indices:** {', '.join(ex['major_indices'])}")
                        maps_link = ex.get("maps_link", "")
                        if maps_link:
                            st.markdown(f"📌 [**View on Google Maps**]({maps_link})")
                        st.divider()

        # --- Stock Indices ---
        with st.expander("📈 Stock Index Values", expanded=True):
            indices = results.get("indices", [])
            if indices and isinstance(indices, list):
                if any(idx.get("sample") for idx in indices if isinstance(idx, dict)):
                    st.info("⚠️ Some index values are fallback/sample data")

                for idx in indices:
                    if isinstance(idx, dict) and "error" not in idx:
                        change = idx.get("change", 0)
                        change_pct = idx.get("change_pct", 0)
                        delta_str = f"{change:+.2f} ({change_pct:+.2f}%)"

                        st.metric(
                            label=f"{idx.get('index_name', 'N/A')} ({idx.get('ticker', '')})",
                            value=f"{idx.get('value', 0):,.2f}",
                            delta=delta_str,
                        )
                        st.caption(f"Exchange: {idx.get('exchange', 'N/A')}")

        # --- Market Summary ---
        with st.expander("📝 Market Overview", expanded=True):
            st.markdown(results.get("market_summary", "N/A"))

        # --- MCP Trace Panel ---
        with st.expander("🔧 MCP Agent Trace (Tool Calls)", expanded=False):
            trace = results.get("trace")
            if trace:
                st.markdown("**Tool Execution Log:**")
                for i, call in enumerate(trace.get_calls()):
                    status_icon = "✅" if call.status == "success" else "❌"
                    st.markdown(f"""
**{i+1}. {status_icon} `{call.tool_name}`**  
- **Inputs:** `{call.inputs}`  
- **Status:** {call.status} | **Duration:** {call.duration_ms}ms  
- **Output preview:** `{str(call.output)[:200]}{'...' if call.output and len(str(call.output)) > 200 else ''}`  
{f'- **Error:** {call.error}' if call.error else ''}
---""")
                st.info(f"Total tool calls: {len(trace.get_calls())}")


# ====================================================================
# FOOTER
# ====================================================================
st.divider()
st.caption("GenAI Lab 12 – MCP-style Travel & Market Intelligence Agent | Powered by Gemini + Streamlit")
