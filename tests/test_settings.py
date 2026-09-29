import json
import stat

from mintsky.core import settings


def test_load_corrupted_settings_is_backed_up(tmp_path, monkeypatch):
    settings_path = tmp_path / "settings.json"
    settings_path.write_text("{invalid json", encoding="utf-8")
    monkeypatch.setattr(settings, "SETTING_FILE", str(settings_path))
    monkeypatch.setattr(settings.keyring, "get_password", lambda *_: None)

    assert settings.load_settings() == {}
    assert (tmp_path / "settings.json.bak").read_text(encoding="utf-8") == "{invalid json"


def test_save_settings_keeps_key_out_of_file_when_keyring_fails(tmp_path, monkeypatch):
    settings_path = tmp_path / "settings.json"
    monkeypatch.setattr(settings, "CONFIG_DIR", str(tmp_path))
    monkeypatch.setattr(settings, "SETTING_FILE", str(settings_path))

    def unavailable(*_args):
        raise RuntimeError("No keyring")

    monkeypatch.setattr(settings.keyring, "set_password", unavailable)
    data = {"theme": "dark", "groq_api_key": "secret"}

    assert settings.save_settings(data) is False
    assert data["groq_api_key"] == "secret"
    assert json.loads(settings_path.read_text(encoding="utf-8")) == {"theme": "dark"}
    assert stat.S_IMODE(settings_path.stat().st_mode) == 0o600


def test_failed_atomic_write_preserves_previous_file(tmp_path):
    from mintsky.core.storage import save_json_atomic

    settings_path = tmp_path / "settings.json"
    settings_path.write_text('{"theme": "dark"}\n', encoding="utf-8")

    try:
        save_json_atomic(settings_path, {"unsupported": object()})
    except TypeError:
        pass
    else:
        raise AssertionError("Unsupported JSON value should raise TypeError")

    assert settings_path.read_text(encoding="utf-8") == '{"theme": "dark"}\n'
    assert list(tmp_path.iterdir()) == [settings_path]
