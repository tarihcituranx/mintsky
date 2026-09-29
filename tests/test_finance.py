import math

import pytest

from mintsky.api.finance import FinanceAPI, parse_price


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (48.9965, 48.9965),
        ("48.9965", 48.9965),
        ("48,9965", 48.9965),
        ("1.234,56", 1234.56),
        ("1,234.56", 1234.56),
        (None, None),
        ("bozuk", None),
        ("nan", None),
        ("inf", None),
    ],
)
def test_parse_price(value, expected):
    result = parse_price(value)
    if expected is None:
        assert result is None
    else:
        assert math.isclose(result, expected)


def test_portfolio_price_preserves_decimal_dot():
    api = FinanceAPI()
    api._data = {
        "USD": {"Type": "Currency", "Buying": "48.9965"},
        "BTC": {"Type": "CryptoCurrency", "TRY_Price": "2.45"},
    }

    assert api.get_rate_price("USD") == pytest.approx(48.9965)
    assert api.get_rate_price("BTC") == pytest.approx(2.45)
