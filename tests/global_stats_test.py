from __future__ import annotations

from collections.abc import Sequence
from typing import Any

import pytest
from trackbear_api.models import Balance
from trackbear_api.models import Stat

from trackbear_cli import global_stats


class MockStatClient:

    def __init__(self, stats: Sequence[Stat]) -> None:
        self._stats = stats
        self._calls: list[dict[str, Any]] = []

    def list(
        self,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> Sequence[Stat]:
        self._calls.append({"start_date": start_date, "end_date": end_date})
        return self._stats


def test_pull_global_stats_default_args() -> None:
    """Test pulling stats with default arguments only."""
    stats = [
        Stat("2026-11-01", Balance(10, 0, 0, 0, 0, 0)),
        Stat("2026-11-30", Balance(10, 0, 0, 0, 0, 0)),
    ]
    mock_client = MockStatClient(stats)

    result = global_stats.pull_global_stats(mock_client)

    assert len(mock_client._calls) == 1
    assert mock_client._calls[0] == {"start_date": None, "end_date": None}

    assert isinstance(result, dict)
    assert result["first_entry"] == "2026-11-01"
    assert result["last_entry"] == "2026-11-30"
    assert result["total_days"] == 30
    assert result["total_entries"] == 2
    assert result["total_word"] == 20
    assert result["total_time"] == 0
    assert result["total_page"] == 0
    assert result["total_chapter"] == 0
    assert result["total_scene"] == 0
    assert result["total_line"] == 0


def test_pull_global_stats_custom_args() -> None:
    """Test pulling stats with custom arguments

    Only validating the call to the client. Return results validated in other tests.
    """
    start_date = "2026-11-10"
    end_date = "2026-11-12"
    stats = [
        Stat("2026-11-01", Balance(10, 0, 0, 0, 0, 0)),
        Stat("2026-11-30", Balance(10, 0, 0, 0, 0, 0)),
    ]
    mock_client = MockStatClient(stats)

    global_stats.pull_global_stats(mock_client, start_date, end_date)

    assert len(mock_client._calls) == 1
    assert mock_client._calls[0] == {"start_date": start_date, "end_date": end_date}


def test_pull_global_stats_no_result() -> None:
    """Raise ValueError if the API returns no results."""
    mock_client = MockStatClient([])

    with pytest.raises(ValueError, match="No results for global stats returned."):
        global_stats.pull_global_stats(mock_client)
