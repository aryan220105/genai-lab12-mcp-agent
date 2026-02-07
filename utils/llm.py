"""
LLM configuration and helper functions.
Priority: Groq (llama-3.3-70b) -> Gemini (2.0 flash) -> Fallback.
"""

import os
from typing import Optional
from groq import Groq

# Try to import google genai; not fatal if missing
try:
    from google import genai as google_genai
    HAS_GOOGLE = True
except ImportError:
    HAS_GOOGLE = False


def _ask_groq(prompt: str) -> Optional[str]:
    """Try Groq API. Returns response text or None on failure."""
    api_key = os.getenv("GROQ_API_KEY", "")
    if not api_key:
        return None
    try:
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2048,
        )
        return response.choices[0].message.content
    except Exception:
        return None


def _ask_gemini(prompt: str) -> Optional[str]:
    """Try Gemini API. Returns response text or None on failure."""
    if not HAS_GOOGLE:
        return None
    api_key = os.getenv("GOOGLE_API_KEY", "")
    if not api_key:
        return None
    try:
        client = google_genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )
        return response.text
    except Exception:
        return None


def ask_gemini(prompt: str) -> str:
    """Send a prompt to the best available LLM.

    Tries Groq first (fast, generous free tier), then Gemini.
    Returns '__LLM_UNAVAILABLE__' if all fail so callers can use fallbacks.

    Args:
        prompt: The text prompt to send.

    Returns:
        The LLM response text, or '__LLM_UNAVAILABLE__'.
    """
    # Try Groq first
    result = _ask_groq(prompt)
    if result:
        return result

    # Try Gemini
    result = _ask_gemini(prompt)
    if result:
        return result

    return "__LLM_UNAVAILABLE__"


def configure_gemini():
    """Legacy compatibility – returns True if any LLM is available."""
    if os.getenv("GROQ_API_KEY", ""):
        return True
    if os.getenv("GOOGLE_API_KEY", ""):
        return True
    return None
