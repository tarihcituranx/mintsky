import json
import stat

from mintsky.core import portfolio


def test_portfolio_round_trip_uses_private_atomic_file(tmp_path, monkeypatch):
    monkeypatch.setattr(portfolio, "CONFIG_DIR", str(tmp_path))
    monkeypatch.setattr(portfolio, "PORTFOLIO_FILE", str(tmp_path / "portfolio.json"))
    items = [{"kod": "USD", "amount": 2, "buy_price": 35}]

    portfolio.save_portfolio(items)

    assert portfolio.load_portfolio() == items
    assert stat.S_IMODE((tmp_path / "portfolio.json").stat().st_mode) == 0o600


def test_portfolio_loader_ignores_invalid_root_shape(tmp_path, monkeypatch):
    path = tmp_path / "portfolio.json"
    path.write_text(json.dumps({"items": {"USD": 1}}), encoding="utf-8")
    monkeypatch.setattr(portfolio, "PORTFOLIO_FILE", str(path))

    assert portfolio.load_portfolio() == []
