"""
Currency & Stock Market Agent – orchestrates tool calls for market intelligence.
Follows MCP-style: plan tools -> execute -> compile results.
Falls back to pre-written content when LLM is unavailable.
"""

from typing import Any, Dict
from utils.trace import MCPTrace
from utils.llm import ask_gemini
from utils.fallbacks import get_fallback_market_summary
from tools.currency_fx import get_currency_info, get_fx_rates
from tools.stocks import get_stock_indices
from tools.exchanges import get_exchange_info


# ---------- MCP Tool Registry ----------
TOOL_REGISTRY = {
    "get_currency_info": get_currency_info,
    "get_fx_rates": get_fx_rates,
    "get_stock_indices": get_stock_indices,
    "get_exchange_info": get_exchange_info,
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


def run_market_agent(country: str, extra_query: str = "") -> Dict[str, Any]:
    """Run the Currency & Stock Market agent pipeline.

    Steps (MCP-style):
      1. get_currency_info(country) – official currency via REST Countries
      2. get_fx_rates(currency_code) – FX conversions
      3. get_exchange_info(country) – exchange names & Google Maps links
      4. get_stock_indices(country) – live index values via yfinance
      5. LLM summary – brief market overview paragraph (with fallback)

    Args:
        country: Country name.
        extra_query: Optional additional query from user.

    Returns:
        Dictionary with all sections and the MCP trace.
    """
    trace = MCPTrace()
    results: Dict[str, Any] = {}

    # --- Step 1: Currency Info ---
    results["currency_info"] = _call_tool(trace, "get_currency_info", country=country)

    # --- Step 2: FX Rates ---
    currency_code = results["currency_info"].get("currency_code", "USD")
    results["fx_rates"] = _call_tool(trace, "get_fx_rates", currency_code=currency_code)

    # --- Step 3: Exchange Info ---
    results["exchanges"] = _call_tool(trace, "get_exchange_info", country=country)

    # --- Step 4: Stock Indices ---
    results["indices"] = _call_tool(trace, "get_stock_indices", country=country)

    # --- Step 5: LLM Market Summary ---
    summary_idx = trace.start_call("llm_market_summary", {
        "country": country,
        "prompt_type": "market_overview"
    })
    try:
        idx_names = [i.get("index_name", "") for i in results.get("indices", []) if isinstance(i, dict)]
        currency_name = results['currency_info'].get('currency_name', 'N/A')

        summary_prompt = f"""Write a brief paragraph (100-150 words) about {country}'s financial market landscape.
Cover: the official currency ({currency_name}), 
major stock exchanges, key indices ({', '.join(idx_names)}), and the country's position 
in global financial markets. 
{('Additional context: ' + extra_query) if extra_query else ''}
Keep it factual and informative."""
        summary_text = ask_gemini(summary_prompt)

        if summary_text == "__LLM_UNAVAILABLE__":
            summary_text = get_fallback_market_summary(country, currency_name, idx_names)
            trace.end_call(summary_idx, "Used pre-written fallback (LLM unavailable)")
        else:
            trace.end_call(summary_idx, summary_text[:200] + "...")

        results["market_summary"] = summary_text
    except Exception as e:
        trace.end_call(summary_idx, None, error=str(e))
        idx_names = [i.get("index_name", "") for i in results.get("indices", []) if isinstance(i, dict)]
        currency_name = results['currency_info'].get('currency_name', 'N/A')
        results["market_summary"] = get_fallback_market_summary(country, currency_name, idx_names)

    # Attach trace
    results["trace"] = trace
    results["meta"] = {"country": country, "extra_query": extra_query}

    return results
