# GenAI Lab 12 – MCP-Style Travel & Market Intelligence Agent

A **Streamlit web application** with two AI-powered tabs that demonstrate **MCP (Model Context Protocol)-style tool orchestration** using LLM reasoning and real-time data APIs.

---

## Features

### Tab 1: Trip Planner Agent
Plan a complete trip with AI-generated insights and real-time data:

| Section | Data Source |
|---|---|
| Cultural & Historic Overview | Groq LLM (Llama 3.3 70B) / Gemini |
| Current Weather | OpenWeather API (live) |
| Weather Forecast (trip dates) | OpenWeather API (live) |
| Flight Options | Sample data generator (clearly labeled) |
| Hotel Options | Sample data generator (clearly labeled) |
| Top Attractions & Places | Curated database + LLM enhancement |
| Day-by-Day Itinerary | Groq LLM / Gemini |
| MCP Trace Panel | Shows all tool calls with inputs, outputs, timing |

### Tab 2: Currency & Stock Market Agent
Get real-time financial intelligence for any supported country:

| Section | Data Source |
|---|---|
| Official Currency (name, code, symbol) | REST Countries API (live) |
| FX Conversion Table (1 unit -> USD/INR/GBP/EUR) | ExchangeRate API (live) |
| Stock Exchange Info + Google Maps Links | Curated database |
| Stock Index Values (with change %) | Yahoo Finance / yfinance (live) |
| Market Overview Paragraph | Groq LLM / Gemini |
| MCP Trace Panel | Shows all tool calls with inputs, outputs, timing |

**Supported countries:** Japan, India, United States, South Korea, China, United Kingdom

---

## Architecture: MCP-Style Tool Orchestration

This project implements an **MCP (Model Context Protocol)-style agent architecture** where the LLM and tools are structured as separate, composable units:

```
User Input
    |
    v
Agent Orchestrator (agent_trip.py / agent_market.py)
    |
    +--> Tool Router (_call_tool)
    |       |
    |       +--> Tool Registry (maps tool names -> functions)
    |       |       |
    |       |       +--> get_current_weather()    [tools/weather.py]
    |       |       +--> get_weather_forecast()   [tools/weather.py]
    |       |       +--> search_flights()         [tools/flights.py]
    |       |       +--> search_hotels()          [tools/hotels.py]
    |       |       +--> get_attractions()        [tools/places.py]
    |       |       +--> get_currency_info()      [tools/currency_fx.py]
    |       |       +--> get_fx_rates()           [tools/currency_fx.py]
    |       |       +--> get_stock_indices()      [tools/stocks.py]
    |       |       +--> get_exchange_info()      [tools/exchanges.py]
    |       |
    |       +--> MCP Trace Logger (utils/trace.py)
    |               Records: tool_name, inputs, output, status, duration_ms
    |
    +--> LLM Calls (utils/llm.py)
    |       Priority: Groq -> Gemini -> Fallback content
    |
    v
Compiled Results + MCP Trace -> Streamlit UI
```

### Key MCP Concepts Implemented:
1. **Tool Schemas** – Every tool has a `TOOL_SCHEMA` dict defining name, description, parameters, and return type
2. **Tool Registry** – A dictionary mapping tool names to callable functions
3. **Tool Router** – `_call_tool()` dispatches tools by name and records execution in the trace
4. **MCP Trace** – `MCPTrace` class records every tool invocation with inputs, outputs, status, and timing
5. **Trace Display** – The UI shows the full MCP trace panel with execution details for transparency

---

## APIs Used

| API | Purpose | Key Required |
|---|---|---|
| **Groq** | Primary LLM (Llama 3.3 70B) | `GROQ_API_KEY` |
| **Google Gemini** | Fallback LLM | `GOOGLE_API_KEY` |
| **OpenWeather** | Current weather + 5-day forecast | `OPENWEATHER_API_KEY` |
| **ExchangeRate-API** | Currency conversion rates | `EXCHANGERATE_API_KEY` |
| **REST Countries** | Official currency info per country | Free (no key) |
| **Yahoo Finance (yfinance)** | Stock index values | Free (no key) |
| **Google Maps** | Exchange HQ location links | Free (URL-based) |

---

## Project Structure

```
GEN AI lab 12/
├── app.py                    # Main Streamlit app (two tabs + sidebar)
├── requirements.txt          # Python dependencies
├── .env.example              # Template for environment variables
├── .gitignore                # Excludes secrets, venv, cache
├── README.md                 # This file
├── SUBMISSION.md             # Deployment & submission guide
├── .streamlit/
│   └── config.toml           # Streamlit theme & server config
├── tools/                    # MCP-style tool functions
│   ├── __init__.py
│   ├── weather.py            # OpenWeather API (current + forecast)
│   ├── flights.py            # Sample flight data generator
│   ├── hotels.py             # Sample hotel data generator
│   ├── places.py             # Attractions (curated + LLM)
│   ├── currency_fx.py        # REST Countries + ExchangeRate API
│   ├── stocks.py             # yfinance stock indices
│   └── exchanges.py          # Exchange info + Google Maps links
└── utils/                    # Agent orchestration & helpers
    ├── __init__.py
    ├── llm.py                # LLM client (Groq -> Gemini -> fallback)
    ├── agent_trip.py          # Trip Planner agent pipeline
    ├── agent_market.py        # Market agent pipeline
    ├── trace.py              # MCP trace tracking class
    └── fallbacks.py          # Pre-written fallback content
```

---

## Setup & Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/aryan220105/genai-lab12-mcp-agent.git
cd genai-lab12-mcp-agent
```

### 2. Create virtual environment & install dependencies

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
# source venv/bin/activate

pip install -r requirements.txt
```

### 3. Set environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
GOOGLE_API_KEY=your_gemini_api_key
OPENWEATHER_API_KEY=your_openweather_api_key
EXCHANGERATE_API_KEY=your_exchangerate_api_key
```

### 4. Run the app

```bash
streamlit run app.py
```

Opens at **http://localhost:8501**

---

## Deploy to Streamlit Community Cloud

### 1. Push to GitHub (see SUBMISSION.md for exact commands)

### 2. Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **"New app"**
3. Select your GitHub repo, branch `main`, main file `app.py`
4. In **Advanced settings → Secrets**, paste:

```toml
GROQ_API_KEY = "your_groq_api_key"
GOOGLE_API_KEY = "your_gemini_api_key"
OPENWEATHER_API_KEY = "your_openweather_api_key"
EXCHANGERATE_API_KEY = "your_exchangerate_api_key"
```

5. Click **Deploy**

---

## Required Secrets (Exact Format for Streamlit Cloud)

In the Streamlit Cloud dashboard → App Settings → Secrets, paste this **exact format**:

```toml
GROQ_API_KEY = "gsk_..."
GOOGLE_API_KEY = "AIza..."
OPENWEATHER_API_KEY = "your_key"
EXCHANGERATE_API_KEY = "your_key"
```

---

## Sample Prompts

### Trip Planner Tab
| From | To | Dates | Budget | Preferences |
|---|---|---|---|---|
| New Delhi | Tokyo | 5 days | Medium | temples, street food, anime |
| Mumbai | Udaipur | 3 days | Budget | lakes, palaces, culture |
| New York | London | 7 days | Luxury | museums, theatre, history |
| Delhi | Paris | 4 days | Medium | art, food, landmarks |

### Currency & Stocks Tab
| Country | What to Expect |
|---|---|
| Japan | JPY, Nikkei 225, TOPIX, Tokyo Stock Exchange map |
| India | INR, SENSEX, NIFTY 50, BSE & NSE map links |
| United States | USD, S&P 500, Dow Jones, NASDAQ, NYSE map |
| South Korea | KRW, KOSPI, KOSDAQ, Korea Exchange map |
| China | CNY, SSE Composite, Hang Seng, 3 exchange maps |
| United Kingdom | GBP, FTSE 100, FTSE 250, LSE map |

---

## Tech Stack

- **Frontend:** Streamlit
- **LLM:** Groq (Llama 3.3 70B) + Google Gemini 2.0 Flash (fallback)
- **Weather:** OpenWeather API
- **Currency:** REST Countries API + ExchangeRate API
- **Stocks:** yfinance (Yahoo Finance)
- **Maps:** Google Maps search links
- **Architecture:** MCP-style tool orchestration with trace logging
