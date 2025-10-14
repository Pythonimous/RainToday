"""Utilities for loading and selecting user-facing weather messages."""
from __future__ import annotations

import json
import random
from pathlib import Path
from typing import Dict, List

_DEFAULT_MESSAGES: Dict[str, List[str]] = {
    "rain": ["YES. Bring an umbrella."],
    "no_rain": ["Nope. Dry as your sense of humor."],
    "maybe": ["Maybe. The clouds are indecisive."],
}


def _messages_path() -> Path:
    """Resolve the path to the messages configuration file."""
    return Path(__file__).resolve().parent.parent / "data" / "messages.json"


def load_messages() -> Dict[str, List[str]]:
    """Load condition-specific messages from disk, falling back to defaults."""
    try:
        with _messages_path().open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except Exception:
        return _DEFAULT_MESSAGES

    if not isinstance(data, dict):
        return _DEFAULT_MESSAGES

    filtered: Dict[str, List[str]] = {
        key: value
        for key, value in data.items()
        if isinstance(value, list) and all(isinstance(item, str) for item in value)
    }
    return filtered or _DEFAULT_MESSAGES


def pick_message(condition: str) -> str:
    """Return a random message for the provided weather condition."""
    messages = load_messages()
    pool = (
        messages.get(condition)
        or _DEFAULT_MESSAGES.get(condition)
        or _DEFAULT_MESSAGES["no_rain"]
    )
    return random.choice(pool)
