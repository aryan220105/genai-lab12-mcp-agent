# GenAI Lab 12 – Submission Guide

## Deployed App URL

> **Streamlit Cloud URL:** `https://genai-lab-mcp-agent-_________.streamlit.app`
>
> *(Fill in after deployment)*

---

## Step 1: Push to GitHub

Open **PowerShell** in the project folder and run these commands **in order**:

```powershell
cd "C:\Users\aryan\OneDrive\Desktop\GEN AI lab 12"

git init

git add .

git commit -m "GenAI Lab 12 - MCP-style Travel and Market Intelligence Agent"

git branch -M main

git remote add origin https://github.com/aryan220105/genai-lab-mcp-agent.git

git push -u origin main
```

> **Note:** If the repo doesn't exist yet, create it first:
> 1. Go to https://github.com/new
> 2. Repository name: `genai-lab-mcp-agent`
> 3. Set to **Public**
> 4. Do NOT initialize with README (we already have one)
> 5. Click **Create repository**
> 6. Then run the git commands above

If `git push` asks for credentials, use a **Personal Access Token** (Settings → Developer settings → Tokens → Generate new token with `repo` scope).

---

## Step 2: Deploy on Streamlit Community Cloud

1. Go to **[share.streamlit.io](https://share.streamlit.io)**
2. Sign in with your **GitHub account** (aryan220105)
3. Click **"New app"**
4. Fill in:
   - **Repository:** `aryan220105/genai-lab-mcp-agent`
   - **Branch:** `main`
   - **Main file path:** `app.py`
5. Click **"Advanced settings"**
6. In the **Secrets** text box, paste this **exact content**:

```toml
GROQ_API_KEY = "your_groq_api_key_here"
GOOGLE_API_KEY = "your_gemini_api_key_here"
OPENWEATHER_API_KEY = "your_openweather_api_key_here"
EXCHANGERATE_API_KEY = "your_exchangerate_api_key_here"
```

> **Tip:** Copy your actual keys from the `.env` file on your local machine.

7. Click **"Deploy!"**
8. Wait 2-3 minutes for the app to build and launch
9. Copy the deployed URL and paste it at the top of this file

---

## Step 3: Screenshots to Submit (6 Screenshots)

### Screenshot 1: Home Screen with Sidebar
- **What to capture:** Full app with both tabs visible, sidebar showing all 4 API keys as green checkmarks (✅)
- **Must show:** Title "GenAI Travel & Market Intelligence Agent", both tab headers, sidebar "API Key Status" section

### Screenshot 2: Trip Planner – Full Output (Top Half)
- **Input:** From: New Delhi → To: Tokyo, 5 days, Medium budget
- **What to capture:** Cultural & Historic Overview paragraph, Current Weather metrics (temp, humidity, wind), Weather Forecast table
- **Must show:** Real weather data from OpenWeather, LLM-generated cultural paragraph

### Screenshot 3: Trip Planner – Full Output (Bottom Half)
- **What to capture:** Flight Options table (labeled SAMPLE), Hotel Options table (labeled SAMPLE), Attractions list, Day-by-Day Itinerary
- **Must show:** All sections populated with data, SAMPLE labels on flights/hotels

### Screenshot 4: Trip Planner – MCP Trace Panel
- **What to capture:** Expanded "MCP Agent Trace (Tool Calls)" section
- **Must show:** All 7 tool calls listed with names, inputs, status (✅), duration, output previews

### Screenshot 5: Currency & Stocks – Full Output
- **Input:** Country: Japan
- **What to capture:** Official Currency (JPY), FX Rates table, Stock Exchanges section with Google Maps link, Stock Index Values (Nikkei 225, TOPIX with change %), Market Overview paragraph
- **Must show:** Real FX rates, real stock values, Google Maps pin link

### Screenshot 6: Currency & Stocks – MCP Trace Panel
- **What to capture:** Expanded "MCP Agent Trace (Tool Calls)" section
- **Must show:** All 5 tool calls listed with names, inputs, status, duration, output previews

---

## Pre-Submission Checklist

Before submitting, verify each item:

- [ ] **App runs locally** – `streamlit run app.py` opens without errors
- [ ] **Sidebar shows all keys green** – All 4 API keys show ✅
- [ ] **Trip Planner works** – Click "Plan My Trip" → all 7 sections populate
- [ ] **Weather is LIVE** – Current weather shows real temperature (not "SAMPLE DATA")
- [ ] **Cultural paragraph is generated** – Not an error message
- [ ] **Itinerary is generated** – Day 1, Day 2, etc. with activities
- [ ] **MCP Trace shows 7 calls** – All marked ✅ success
- [ ] **Currency & Stocks works** – Click "Get Market Info" → all 5 sections populate
- [ ] **FX rates are LIVE** – Real conversion rates (not fallback)
- [ ] **Stock indices show values** – Nikkei, SENSEX, etc. with change %
- [ ] **Google Maps link works** – Clicking the link opens Google Maps
- [ ] **MCP Trace shows 5 calls** – All marked ✅ success
- [ ] **GitHub repo is public** – https://github.com/aryan220105/genai-lab-mcp-agent
- [ ] **No API keys in code** – Keys only in .env (gitignored) and Streamlit secrets
- [ ] **Streamlit Cloud deployed** – App accessible via public URL
- [ ] **6 screenshots taken** – All items listed above are captured
- [ ] **README.md is complete** – Setup steps, architecture, sample prompts documented

---

## Quick Reference: What Each Tab Demonstrates

### Trip Planner Tab (7 MCP Tool Calls)
1. `llm_cultural_paragraph` → Groq/Gemini LLM
2. `get_current_weather` → OpenWeather API
3. `get_weather_forecast` → OpenWeather API
4. `search_flights` → Sample data generator
5. `search_hotels` → Sample data generator
6. `get_attractions` → Curated database
7. `llm_day_itinerary` → Groq/Gemini LLM

### Currency & Stocks Tab (5 MCP Tool Calls)
1. `get_currency_info` → REST Countries API
2. `get_fx_rates` → ExchangeRate API
3. `get_exchange_info` → Curated database
4. `get_stock_indices` → Yahoo Finance (yfinance)
5. `llm_market_summary` → Groq/Gemini LLM
