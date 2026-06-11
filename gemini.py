import os
import time
import json
import re
from typing import Any, Dict

from dotenv import load_dotenv
import google.generativeai as genai

from prompts import build_prompt, validate_and_fix, fallback_response

# Configure the SDK once at module import; acceptable if GEMINI_API_KEY is absent.
load_dotenv()
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))


def _strip_fences(text: str) -> str:
    """Remove common markdown fences from a model response, including language tags like `json`."""
    # Capture inner content of fenced blocks like ```json ... ``` and replace with inner text.
    def _unfence(m: re.Match) -> str:
        return m.group(1).strip()

    pattern = re.compile(r"```(?:\w+)?\s*([\s\S]*?)```")
    return pattern.sub(_unfence, text).strip()


def _extract_json_substring(text: str) -> str:
    """Extract the first JSON object substring from text using braces."""
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end < start:
        raise ValueError("no JSON object found")
    return text[start : end + 1]


def _get_text_from_response(resp: Any) -> str:
    """Safely extract text content from various SDK response shapes."""
    if resp is None:
        return ""
    # Response may expose .text
    if hasattr(resp, "text"):
        return getattr(resp, "text") or ""
    # Or be a dict-like structure
    if isinstance(resp, dict):
        for key in ("text", "content", "output"):
            if key in resp and isinstance(resp[key], str):
                return resp[key]
        cand = resp.get("candidates") or resp.get("outputs")
        if isinstance(cand, list) and cand:
            first = cand[0]
            if isinstance(first, dict):
                return first.get("content") or first.get("text") or ""
    return str(resp)


def analyze_code(problem: str, code: str, language: str) -> Dict[str, str]:
    """Call Gemini to analyze code and return a validated dict matching the schema."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return fallback_response("GEMINI_API_KEY not set")

    model = genai.GenerativeModel("gemini-3.1-flash-lite")
    prompt = build_prompt(problem=problem, code=code, language=language)

    backoffs = [1, 2, 4]
    last_err = ""
    for attempt in range(3):
        try:
            resp = model.generate_content(prompt)
            raw = _get_text_from_response(resp)
            raw = _strip_fences(raw)
            json_text = _extract_json_substring(raw)
            parsed = json.loads(json_text)
            return validate_and_fix(parsed)
        except Exception as e:
            last_err = str(e)
            if attempt < 2:
                time.sleep(backoffs[attempt])
            continue

    return fallback_response(f"gemini failed: {last_err}")
