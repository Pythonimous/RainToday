import pytest

from src.services import geocode


class _DummyResponse:
    """Minimal mock for requests.Response used by the geocode helper."""

    def __init__(self, payload, status_code=200):
        self._payload = payload
        self.status_code = status_code

    def json(self):
        return self._payload


@pytest.mark.unit
def test_geocode_returns_first_result(monkeypatch):
    payload = {"results": [{"latitude": 51.5074, "longitude": -0.1278, "name": "London"}]}

    def fake_get(url, params, timeout):  # pragma: no cover - simple shim
        return _DummyResponse(payload)

    monkeypatch.setattr(geocode.requests, "get", fake_get)

    result = geocode.search_city("London")

    assert result["lat"] == 51.5074
    assert result["lon"] == -0.1278
    assert result["name"] == "London"


@pytest.mark.unit
def test_geocode_handles_missing_results(monkeypatch):
    def fake_get(url, params, timeout):  # pragma: no cover - simple shim
        return _DummyResponse({"results": []})

    monkeypatch.setattr(geocode.requests, "get", fake_get)

    with pytest.raises(geocode.CityNotFoundError):
        geocode.search_city("Nowhereville")


@pytest.mark.unit
def test_geocode_handles_request_failure(monkeypatch):
    def fake_get(url, params, timeout):  # pragma: no cover - simple shim
        raise RuntimeError("connection error")

    monkeypatch.setattr(geocode.requests, "get", fake_get)

    with pytest.raises(geocode.GeocodeServiceError):
        geocode.search_city("London")


@pytest.mark.unit
def test_geocode_handles_http_404(monkeypatch):
    def fake_get(url, params, timeout):
        return _DummyResponse({}, status_code=404)

    monkeypatch.setattr(geocode.requests, "get", fake_get)

    with pytest.raises(geocode.CityNotFoundError):
        geocode.search_city("Paris")


@pytest.mark.unit
def test_geocode_rejects_malformed_payload(monkeypatch):
    class BadResponse:
        status_code = 200

        def json(self):
            raise ValueError("bad payload")

    monkeypatch.setattr(geocode.requests, "get", lambda *args, **kwargs: BadResponse())

    with pytest.raises(geocode.GeocodeServiceError):
        geocode.search_city("Lisbon")
