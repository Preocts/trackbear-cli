from __future__ import annotations

import pytest

from trackbear_cli import _auth


@pytest.mark.parametrize(
    "token,expected",
    (
        ("abc", True),
        (123, False),
    ),
)
def test_save(token: str, expected: bool) -> None:
    """Test the logic of the save command."""
    result = _auth.save(token)

    assert result is expected


def test_clear_successful() -> None:
    """Test a successful clear command logic."""
    result = _auth.clear()

    assert result is True


def test_clear_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test a failed clear command logic."""
    # Set the default blank value to an invalid non-string to trigger an exception.
    monkeypatch.setattr(_auth, "_BLANK_VALUE", 1234)

    result = _auth.clear()

    assert result is False
