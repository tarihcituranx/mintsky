from mintsky.utils import (
    fmt_date,
    fmt_dt,
    fmt_pct,
    fmt_time,
    fmt_try,
    val,
    wind_level_key,
    yon,
)


def test_formatters_handle_normal_and_missing_values():
    assert fmt_try(1234.5) == "1.234,50 ₺"
    assert fmt_try(None) == "—"
    assert fmt_pct(2.5) == "+2.50%"
    assert fmt_pct(-1) == "-1.00%"
    assert fmt_pct(None) == "—"
    assert val(None) == "—"
    assert val(12.4) == "12"


def test_date_and_time_formatters_survive_bad_api_values():
    assert fmt_date("not-a-date") == "not-a-date"
    assert fmt_time("not-a-time") == "not-a-time"
    assert fmt_date(None) is None
    assert fmt_time(None) == "None"


def test_utc_api_timestamps_are_always_shown_in_turkey_time():
    assert fmt_time("2026-09-29T10:09:00.000Z") == "13:09"
    assert fmt_dt("2026-09-29T10:09:00.000Z") == "29.09.2026 13:09"


def test_wind_direction_rejects_invalid_values():
    assert yon(None) == ""
    assert yon(-9999) == ""
    assert yon("north") == ""
    assert yon(0)


def test_wind_level_matches_the_mgm_guide_boundaries():
    assert wind_level_key(0) == "wind_calm"
    assert wind_level_key(5.9) == "wind_breeze"
    assert wind_level_key(6) == "wind_light"
    assert wind_level_key(20) == "wind_moderate"
    assert wind_level_key(103) == "wind_hurricane"
    assert wind_level_key(-1) is None
