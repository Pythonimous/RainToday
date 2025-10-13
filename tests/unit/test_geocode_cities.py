import pytest
from fastapi import HTTPException

from app import main


class _DummyResponse:
    """Minimal mock for requests.Response used by the geocode helper."""

    def __init__(self, payload):
        self._payload = payload

    def json(self):
        return self._payload


@pytest.mark.unit
def test_geocode_returns_first_result(monkeypatch):
    payload = {"results": [{"latitude": 51.5074, "longitude": -0.1278, "name": "London"}]}

    def fake_get(url, params, timeout):  # pragma: no cover - simple shim
        return _DummyResponse(payload)

    monkeypatch.setattr(main.requests, "get", fake_get)

    result = main.geocode("London")

    assert result["lat"] == 51.5074
    assert result["lon"] == -0.1278
    assert result["name"] == "London"


@pytest.mark.unit
def test_geocode_handles_missing_results(monkeypatch):
    def fake_get(url, params, timeout):  # pragma: no cover - simple shim
        return _DummyResponse({"results": []})

    monkeypatch.setattr(main.requests, "get", fake_get)

    with pytest.raises(HTTPException) as exc_info:
        main.geocode("Nowhereville")

    assert exc_info.value.status_code == 404


@pytest.mark.unit
def test_geocode_handles_request_failure(monkeypatch):
    def fake_get(url, params, timeout):  # pragma: no cover - simple shim
        raise RuntimeError("connection error")

    monkeypatch.setattr(main.requests, "get", fake_get)

    with pytest.raises(HTTPException) as exc_info:
        main.geocode("London")

    assert exc_info.value.status_code == 502
