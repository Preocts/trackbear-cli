"""CLI routes for Global Stats."""

from __future__ import annotations

import datetime

import cyclopts
from trackbear_api import TrackBearClient

from trackbear_cli import _global_stats
from trackbear_cli._config import get_config

commands = cyclopts.App(name="stats")


@commands.command
def total(start_date: str | None = None, end_date: str | None = None) -> int:
    """Fetch total stats for the given dates.

    Args:
        start_date (str): YYYY-MM-DD format date of when to start pulling stats (Default: beginning of time)
        end_date (str): YYYY-MM-DD format date of when to stop pulling stats (Default: now)

    Returns:
        int: Value of exit code
    """
    try:
        if start_date:
            datetime.date.fromisoformat(start_date)
        if end_date:
            datetime.date.fromisoformat(end_date)

    except ValueError:
        print("Invalid date provided.")
        return 1

    config = get_config()

    client = TrackBearClient("TBD", api_token=config.auth_token)

    try:
        result = _global_stats._pull_global_stats(client.stat, start_date, end_date)

    except ValueError:
        print("No results returned.")
        return 1

    else:
        print(result)

    return 0
