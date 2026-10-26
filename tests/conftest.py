from __future__ import annotations

import json
import pathlib

import pytest

from trackbear_cli import _config as config

MOCK_CONFIG_NAME = "mockconfig.json"
MOCK_DEFAULT_CONFIG = {
    "auth_token": "this_is_a_mock_token",
}


@pytest.fixture(autouse=True)
def filepath(tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Create a mock config to use for tests and patches that path into _config.py"""
    config.get_config.cache_clear()
    _filepath = tmp_path / MOCK_CONFIG_NAME
    json.dump(MOCK_DEFAULT_CONFIG, _filepath.open("w", encoding="utf-8"), indent=2)

    monkeypatch.setattr(config, "_FILEPATH", _filepath)
