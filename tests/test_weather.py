import os
from unittest.mock import patch

import pytest

from mintsky.api.weather import WeatherAPI


@patch("mintsky.api.weather.requests.get")
def test_fetch_weather_empty_response(mock_get):
    class MockResponse:
        def __init__(self, json_data, status_code=200):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

        def raise_for_status(self):
            pass

    mock_get.return_value = MockResponse([])

    success, msg, data = WeatherAPI.fetch_weather("Adana", "Seyhan")
    assert success is False
    assert "MGM API boş veya geçersiz yanıt döndürdü" in msg or "Bağlantı" in msg
    assert data is None


@patch("mintsky.api.weather.requests.get")
def test_fetch_weather_invalid_json(mock_get):
    class MockResponse:
        def __init__(self, text):
            self.text = text
            self.status_code = 200

        def json(self):
            import json

            return json.loads(self.text)

        def raise_for_status(self):
            pass

    mock_get.return_value = MockResponse("invalid json")

    success, msg, data = WeatherAPI.fetch_weather("Adana", "Seyhan")
    assert success is False
    assert "Bağlantı Hatası" in msg
    assert data is None
