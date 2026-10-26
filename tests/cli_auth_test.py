from __future__ import annotations

import pytest

from trackbear_cli import _auth
from trackbear_cli import cli_auth


def test_save_cli_success(
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test the CLI command for a success."""
    monkeypatch.setattr(_auth, "save", lambda token: True)

    result = cli_auth.commands("save thisismebreathing", result_action="return_value")

    assert result == 0
    assert capsys.readouterr().out == "Saved the new token ***hing\n"


def test_save_cli_failure(
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test the CLI command for a failure."""
    monkeypatch.setattr(_auth, "save", lambda token: False)

    result = cli_auth.commands("save thisismebreathing", result_action="return_value")

    assert result == 1
    assert capsys.readouterr().out == "Failed to save token.\n"


def test_clear_cli_success(
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test the CLI command for a success."""
    monkeypatch.setattr(_auth, "clear", lambda: True)

    result = cli_auth.commands("clear", result_action="return_value")

    assert result == 0
    assert capsys.readouterr().out == "The token has been cleared.\n"


def test_clear_cli_failure(
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test the CLI command for a failure."""
    monkeypatch.setattr(_auth, "clear", lambda: False)

    result = cli_auth.commands("clear", result_action="return_value")

    assert result == 1
    assert capsys.readouterr().out == "Unable to clear token.\n"
