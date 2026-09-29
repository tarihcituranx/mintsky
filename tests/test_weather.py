"""
Weather API Tests — boş / hatalı yanıt senaryoları.

Fallback davranışı:
  fetch_weather boş MGM yanıtı alınca Nominatim'e geçer;
  Nominatim da boş döndüğünde False döner.
  Bu testi ikinci aşamayı da mock'layarak doğrularız.
"""

import json
from unittest.mock import MagicMock, patch

import pytest

from mintsky.api.weather import WeatherAPI


def test_nearest_center_skips_invalid_coordinates():
    centers = [
        {"il": "bad", "enlem": None, "boylam": 40},
        {"il": "Ankara", "ilce": "Çankaya", "enlem": 39.9, "boylam": 32.8},
        {"il": "İstanbul", "ilce": "Kadıköy", "enlem": 40.98, "boylam": 29.1},
    ]

    nearest = WeatherAPI.nearest_center(centers, 39.91, 32.85)

    assert nearest["il"] == "Ankara"


def test_current_meteoalarm_schema_matches_town_center_ids():
    alerts = [
        {
            "towns": {"yellow": [123], "orange": [], "red": []},
            "text": {"yellow": "İlçe için kuvvetli yağış uyarısı."},
            "weather": {"yellow": ["thunderstorm"]},
            "end": "2026-09-29T18:00:00Z",
        },
        {
            "towns": {"yellow": [456], "orange": [], "red": []},
            "text": {"yellow": "Başka ilçe uyarısı."},
            "weather": {"yellow": ["rain"]},
        },
    ]

    result = WeatherAPI.meteoalerts_for_center(alerts, "123")

    assert len(result) == 1
    assert result[0]["level"] == "yellow"
    assert result[0]["description"] == "İlçe için kuvvetli yağış uyarısı."
    assert WeatherAPI.meteoalerts_for_center(alerts, "bad") == []


@patch("mintsky.api.weather.session.get")
def test_fetch_weather_empty_response(mock_get):
    """MGM ve Nominatim her ikisi de boş dönünce False beklenir."""
    empty = MagicMock()
    empty.text = "[]"
    empty.status_code = 200
    empty.json.return_value = []
    # Her iki çağrıda da boş döner (MGM + Nominatim fallback)
    mock_get.return_value = empty

    success, msg, data = WeatherAPI.fetch_weather("Adana", "Seyhan")
    assert success is False
    assert data is None


@patch("mintsky.api.weather.session.get")
def test_fetch_weather_invalid_json(mock_get):
    """JSON parse hatası exception'a, exception False'a dönüşmeli."""
    bad = MagicMock()
    bad.text = "invalid json"
    bad.status_code = 200
    bad.json.side_effect = ValueError("No JSON")

    mock_get.return_value = bad

    success, msg, data = WeatherAPI.fetch_weather("Adana", "Seyhan")
    assert success is False
    assert data is None


@patch("mintsky.api.weather.session.get")
def test_fetch_weather_valid_mgm(mock_get):
    """Geçerli MGM yanıtı True döndürmeli."""
    good_center = MagicMock()
    good_center.text = json.dumps(
        [
            {
                "merkezId": 1,
                "il": "Adana",
                "ilce": "Seyhan",
                "enlem": 37.0,
                "boylam": 35.3,
                "gunlukTahminIstNo": 1,
                "saatlikTahminIstNo": 1,
            }
        ]
    )
    good_center.status_code = 200
    good_center.json.return_value = json.loads(good_center.text)

    empty_detail = MagicMock()
    empty_detail.text = "[]"
    empty_detail.status_code = 200
    empty_detail.json.return_value = []

    # İlk çağrı merkezler, geri kalanlar detay/alarm
    mock_get.side_effect = [good_center] + [empty_detail] * 20

    with patch.object(WeatherAPI, "fetch_openmeteo", return_value={}), patch.object(
        WeatherAPI, "fetch_msn", return_value={}
    ):
        success, msg, data = WeatherAPI.fetch_weather("Adana", "Seyhan")
    assert success is True
    assert data is not None
