from __future__ import annotations

import json
import pathlib

import pytest

from trackbear_cli import _config as config
from trackbear_cli import cli_auth

MOCK_CONFIG_NAME = "mockconfig.json"
MOCK_DEFAULT_CONFIG = {
    "auth_token": "this_is_a_mock_token",
}


@pytest.fixture(autouse=True)
def filepath(tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> pathlib.Path:
    """Create a mock config to use for tests and patches that path into _config.py"""
    _filepath = tmp_path / MOCK_CONFIG_NAME
    json.dump(MOCK_DEFAULT_CONFIG, _filepath.open("w", encoding="utf-8"), indent=2)

    monkeypatch.setattr(config, "_FILEPATH", _filepath)

    return _filepath


def test_save_cli_success(
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test the CLI command for a success."""
    monkeypatch.setattr(cli_auth, "_save", lambda token: True)

    result = cli_auth.commands("save thisismebreathing", result_action="return_value")

    assert result == 0
    assert capsys.readouterr().out == "Saved the new token ***hing\n"


def test_save_cli_failure(
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test the CLI command for a failure."""
    monkeypatch.setattr(cli_auth, "_save", lambda token: False)

    result = cli_auth.commands("save thisismebreathing", result_action="return_value")

    assert result == 1
    assert capsys.readouterr().out == "Failed to save token.\n"


@pytest.mark.parametrize(
    "token,expected",
    (
        ("abc", True),
        (123, False),
    ),
)
def test_save(token: str, expected: bool) -> None:
    """Test the logic of the save command."""
    result = cli_auth._save(token)

    assert result is expected


def test_clear_cli_success(
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test the CLI command for a success."""
    monkeypatch.setattr(cli_auth, "_clear", lambda: True)

    result = cli_auth.commands("clear", result_action="return_value")

    assert result == 0
    assert capsys.readouterr().out == "The token has been cleared.\n"


def test_clear_cli_failure(
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test the CLI command for a failure."""
    monkeypatch.setattr(cli_auth, "_clear", lambda: False)

    result = cli_auth.commands("clear", result_action="return_value")

    assert result == 1
    assert capsys.readouterr().out == "Unable to clear token.\n"


def test_clear_successful() -> None:
    """Test a successful clear command logic."""
    result = cli_auth._clear()

    assert result is True


def test_clear_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test a failed clear command logic."""
    # Set the default blank value to an invalid non-string to trigger an exception.
    monkeypatch.setattr(cli_auth, "_BLANK_VALUE", 1234)

    result = cli_auth._clear()

    assert result is False
