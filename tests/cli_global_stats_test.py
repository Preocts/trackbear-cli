from __future__ import annotations

import json
import pathlib

import pytest
from trackbear_api import TrackBearClient

from trackbear_cli import _config as config
from trackbear_cli import _global_stats
from trackbear_cli import cli_global_stats

MOCK_CONFIG_NAME = "mockconfig.json"
MOCK_DEFAULT_CONFIG = {
    "auth_token": "this_is_a_mock_token",
}


class MockController:

    def __init__(self, global_stats: dict[str, str], raises: Exception | None = None) -> None:
        self._global_stats = global_stats
        self._raises = raises

    def pull_global_stats(
        self,
        client: TrackBearClient,
        start_date: str | None,
        end_date: str | None,
    ) -> dict[str, str]:
        if self._raises:
            raise self._raises

        self._global_stats_start_date = start_date
        self._global_stats_end_date = end_date
        return self._global_stats


@pytest.fixture(autouse=True)
def filepath(tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> pathlib.Path:
    """Create a mock config to use for tests and patches that path into _config.py"""
    _filepath = tmp_path / MOCK_CONFIG_NAME
    json.dump(MOCK_DEFAULT_CONFIG, _filepath.open("w", encoding="utf-8"), indent=2)

    monkeypatch.setattr(config, "_FILEPATH", _filepath)

    return _filepath


@pytest.mark.parametrize(
    "start_date,end_date",
    (
        (None, None),
        ("2026-11-01", None),
        (None, "2026-11-01"),
        ("2026-11-01", "2026-11-30"),
    ),
)
def test_total_success(
    start_date: str | None,
    end_date: str | None,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test the total command for success."""

    mock_controller = MockController({"foo": "bar"})

    monkeypatch.setattr(_global_stats, "_pull_global_stats", mock_controller.pull_global_stats)

    command = ["total"]
    if start_date:
        command.extend(["--start-date", start_date])

    if end_date:
        command.extend(["--end-date", end_date])

    result = cli_global_stats.commands(command, result_action="return_value")

    assert result == 0
    assert capsys.readouterr().out == "{'foo': 'bar'}\n"

    assert mock_controller._global_stats_start_date == start_date
    assert mock_controller._global_stats_end_date == end_date


@pytest.mark.parametrize(
    "start_date,end_date",
    (
        ("foo", "2026-11-30"),
        ("2026-11-01", "foo"),
        ("2026-11-00", "2026-11-30"),
        ("2026-11-01", "2026-11-31"),
    ),
)
def test_total_invalid_date(
    start_date: str,
    end_date: str,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Handle invalid date being provided from CLI."""
    mock_controller = MockController({"foo": "bar"})
    monkeypatch.setattr(_global_stats, "_pull_global_stats", mock_controller.pull_global_stats)

    command = ["total", "--start-date", start_date, "--end-date", end_date]

    result = cli_global_stats.commands(command, result_action="return_value")

    assert result == 1
    assert capsys.readouterr().out == "Invalid date provided.\n"


def test_total_handles_no_results(
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Handle controller raising ValueError on no results."""
    mock_controller = MockController({"foo": "bar"}, ValueError("boom"))
    monkeypatch.setattr(_global_stats, "_pull_global_stats", mock_controller.pull_global_stats)

    result = cli_global_stats.commands("total", result_action="return_value")

    assert result == 1
    assert capsys.readouterr().out == "No results returned.\n"
