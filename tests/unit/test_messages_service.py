import json

import pytest

from src.services import messages


@pytest.mark.unit
def test_pick_message_uses_custom_file(tmp_path, monkeypatch):
    custom = tmp_path / "messages.json"
    custom.write_text(json.dumps({"rain": ["Custom rain message"]}), encoding="utf-8")

    monkeypatch.setattr(messages, "_messages_path", lambda: custom)
    monkeypatch.setattr(messages.random, "choice", lambda seq: seq[0])

    result = messages.pick_message("rain")
    assert result == "Custom rain message"


@pytest.mark.unit
def test_pick_message_falls_back_for_unknown_condition(tmp_path, monkeypatch):
    custom = tmp_path / "missing.json"

    monkeypatch.setattr(messages, "_messages_path", lambda: custom)
    monkeypatch.setattr(messages.random, "choice", lambda seq: seq[0])

    result = messages.pick_message("unknown")
    assert result in {
        "Nope. Dry as your sense of humor.",
        "YES. Bring an umbrella.",
        "Maybe. The clouds are indecisive.",
    }


@pytest.mark.unit
def test_load_messages_filters_invalid_entries(tmp_path, monkeypatch):
    custom = tmp_path / "messages.json"
    custom.write_text(
        json.dumps({"rain": ["Valid"], "maybe": "not-a-list", "extra": ["ok", 123]}),
        encoding="utf-8",
    )

    monkeypatch.setattr(messages, "_messages_path", lambda: custom)

    loaded = messages.load_messages()
    assert "rain" in loaded
    assert loaded["rain"] == ["Valid"]
    assert "maybe" not in loaded
    assert "extra" not in loaded
