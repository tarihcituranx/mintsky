import pytest
import os
import json
from unittest.mock import patch
from mintsky.core.settings import load_settings, save_settings
from mintsky.constants import SETTING_FILE

def test_settings_corruption(tmp_path):
    # Mocking SETTING_FILE directly would require patching the constant,
    # but since it's already imported, we will just patch it in the module.
    pass

@patch("mintsky.core.settings.SETTING_FILE", "/tmp/mock_settings.json")
def test_load_corrupted_settings():
    with open("/tmp/mock_settings.json", "w") as f:
        f.write("{invalid json")
    
    data = load_settings()
    assert data == {}
    assert os.path.exists("/tmp/mock_settings.json.bak")
    
    if os.path.exists("/tmp/mock_settings.json"): os.remove("/tmp/mock_settings.json")
    if os.path.exists("/tmp/mock_settings.json.bak"): os.remove("/tmp/mock_settings.json.bak")

@patch("mintsky.core.settings.keyring.set_password")
@patch("mintsky.core.settings.SETTING_FILE", "/tmp/mock_settings.json")
def test_save_settings_keyring_fail(mock_set_password):
    mock_set_password.side_effect = Exception("No keyring")
    
    data = {"theme": "dark", "groq_api_key": "123"}
    success = save_settings(data)
    
    assert success is False
    with open("/tmp/mock_settings.json", "r") as f:
        saved_data = json.load(f)
    assert "groq_api_key" not in saved_data
    assert saved_data["theme"] == "dark"
    
    if os.path.exists("/tmp/mock_settings.json"): os.remove("/tmp/mock_settings.json")
