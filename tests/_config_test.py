from __future__ import annotations

import copy
import json
import pathlib

import pytest

from trackbear_cli import _config as config

MOCK_CONFIG_NAME = "mockconfig.json"
MOCK_DEFAULT_CONFIG = {
    "auth_token": "this_is_a_mock_token",
}
MOCK_MODIFIED_CONFIG = {
    "auth_token": "1egg3wheat2sugar3milk",
}


@pytest.fixture
def filepath(tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> pathlib.Path:
    """Create a mock config to use for tests and patches that path into _config.py"""
    _filepath = tmp_path / MOCK_CONFIG_NAME
    json.dump(MOCK_DEFAULT_CONFIG, _filepath.open("w", encoding="utf-8"), indent=2)

    monkeypatch.setattr(config, "_FILEPATH", _filepath)

    return _filepath


def test_load_creates_file(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: pathlib.Path,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Loading without an existing file should create that file."""
    filepath = tmp_path / MOCK_CONFIG_NAME
    assert not filepath.exists()

    monkeypatch.setattr(config, "_FILEPATH", filepath)

    with caplog.at_level("INFO"):
        newconfig = config.Config()
        newconfig.load()

    assert filepath.exists()
    contents = json.load(filepath.open())
    assert contents == config._DEFAULT_CONFIG


def test_validation_of_auth_token_string(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: pathlib.Path,
) -> None:
    """Loading without an existing file should create that file."""
    badconfig = copy.deepcopy(MOCK_DEFAULT_CONFIG)
    badconfig["auth_token"] = 123  # type: ignore
    filepath = tmp_path / MOCK_CONFIG_NAME
    json.dump(badconfig, filepath.open("w", encoding="utf-8"), indent=2)
    monkeypatch.setattr(config, "_FILEPATH", filepath)
    newconfig = config.Config()

    with pytest.raises(ValueError, match="The TrackBear Auth token must be a string value"):
        newconfig.load()


@pytest.mark.usefixtures("filepath")
def test_load() -> None:
    """Test loading when the file exists."""
    newconfig = config.Config()

    newconfig.load()

    for key, value in MOCK_DEFAULT_CONFIG.items():
        configattr = getattr(newconfig, key)
        assert configattr == value


@pytest.mark.usefixtures("filepath")
def test_save() -> None:
    """Test saving values to file."""
    saveconfig = config.Config(**MOCK_MODIFIED_CONFIG)
    loadconfig = config.Config()

    saveconfig.save()
    loadconfig.load()

    assert loadconfig.auth_token == MOCK_MODIFIED_CONFIG["auth_token"]
