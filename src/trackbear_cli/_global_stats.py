from __future__ import annotations

import dataclasses
import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence
    from typing import Protocol

    from trackbear_api.models import Stat

    class _StatClient(Protocol):
        def list(
            self,
            start_date: str | None = None,
            end_date: str | None = None,
        ) -> Sequence[Stat]: ...


def _pull_global_stats(
    client: _StatClient,
    since: str | None = None,
    until: str | None = None,
) -> dict[str, str]:
    """Pull global stats from TrackBear API.

    Args:
        since (str): YYYY-MM-DD format date of when to start pulling stats (Default: beginning of time)
        until (str): YYYY-MM-DD format date of when to stop pulling stats (Default: now)

    Raises:
        ValueError: When no results are returned from the API.
    """
    results = client.list(start_date=since, end_date=until)

    if not results:
        raise ValueError("No results for global stats returned.")

    first_date = datetime.date.fromisoformat(results[0].date)
    last_date = datetime.date.fromisoformat(results[-1].date)

    balance = {key: 0 for key in dataclasses.asdict(results[0].counts).keys()}

    for result in results:
        for key in balance.keys():
            balance[key] += getattr(result.counts, key)

    parsed_results = {
        "since": since if since is not None else results[0].date,
        "until": until if until is not None else results[-1].date,
        "first_entry": results[0].date,
        "last_entry": results[-1].date,
        "days": str((last_date - first_date).days + 1),
        "entries": str(len(results)),
        **{k: str(v) for k, v in balance.items()},
    }

    return parsed_results
