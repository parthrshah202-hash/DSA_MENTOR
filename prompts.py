import json
from typing import Any, Dict, List

JSON_KEYS: List[str] = [
    "topic_badge",
    "bug_detected",
    "hint_1",
    "hint_2",
    "time_complexity",
    "space_complexity",
]


def build_prompt(problem: str, code: str, language: str = "Python") -> str:
    """Build the instruction prompt to send to Gemini (requests raw JSON only)."""
    prompt = (
        "You are an assistant that MUST reply with raw JSON only, no markdown, no "
        "explanations, no code fences, and no trailing text. Produce a single JSON "
        "object with the exact keys and string values listed below (no extra keys):\n\n"
        f"{json.dumps({k: 'string' for k in JSON_KEYS}, indent=2)}\n\n"
        "Interpretation:\n"
        "- topic_badge: short DSA topic tag (e.g., 'two-pointers')\n"
        "- bug_detected: short description or 'none'\n"
        "- hint_1: first Socratic hint (concise)\n"
        "- hint_2: second hint (concise)\n"
        "- time_complexity: estimated time complexity (e.g., 'O(n log n)')\n"
        "- space_complexity: estimated space complexity (e.g., 'O(1)')\n\n"
        "Respond only with the JSON object. Now analyze the problem and the code "
        "provided and produce the JSON.\n\n"
        f"LANGUAGE: {language}\n\n"
        "PROBLEM STATEMENT:\n"
        f"{problem}\n\n"
        "USER CODE:\n"
        f"{code}\n"
    )
    return prompt


def fallback_response(error: str) -> Dict[str, str]:
    """Return a fallback response dict with the given error in every field."""
    return {k: f"ERROR: {error}" for k in JSON_KEYS}


def validate_and_fix(parsed: Any) -> Dict[str, str]:
    """Validate parsed JSON-like object and return a dict matching the exact schema; on problems, return a fallback with errors."""
    if not isinstance(parsed, dict):
        return fallback_response("response is not a JSON object")
    out: Dict[str, str] = {}
    for k in JSON_KEYS:
        v = parsed.get(k)
        if isinstance(v, str):
            out[k] = v
        else:
            out[k] = f"ERROR: missing or invalid field '{k}'"
    return out
