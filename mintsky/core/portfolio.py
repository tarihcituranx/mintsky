import json
import os

from mintsky.constants import CONFIG_DIR, PORTFOLIO_FILE
from mintsky.core.storage import save_json_atomic


def load_portfolio():
    try:
        with open(PORTFOLIO_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            items = data.get("items", [])
            return items if isinstance(items, list) else []
    except Exception:
        return []


def save_portfolio(items):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    save_json_atomic(PORTFOLIO_FILE, {"items": items})
