from __future__ import annotations

import datetime

from trackbear_api import TrackBearClient

_APP_NAME = "trackbear-cli"


def pull_global_stats(
    client: TrackBearClient,
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
    results = client.stat.list(start_date=since, end_date=until)

    if not results:
        raise ValueError("No results for global stats returned.")

    first_date = datetime.date.fromisoformat(results[0].date)
    last_date = datetime.date.fromisoformat(results[-1].date)

    parsed_results: dict[str, str | int] = {
        "first_entry": results[0].date,
        "last_entry": results[-1].date,
        "total_days": (last_date - first_date).days + 1,
        "total_entries": len(results),
        "total_word": 0,
        "total_time": 0,
        "total_page": 0,
        "total_chapter": 0,
        "total_scene": 0,
        "total_line": 0,
    }

    for result in results:
        parsed_results["total_word"] += result.counts.word
        parsed_results["total_time"] += result.counts.time
        parsed_results["total_page"] += result.counts.page
        parsed_results["total_chapter"] += result.counts.chapter
        parsed_results["total_scene"] += result.counts.scene
        parsed_results["total_line"] += result.counts.line

    return parsed_results


def main() -> None:
    client = TrackBearClient(_APP_NAME)

    thirty_days = datetime.datetime.now() - datetime.timedelta(days=30)
    thirty_days_since = thirty_days.strftime("%Y-%m-%d")

    stats = pull_global_stats(client)
    for key, value in stats.items():
        if value:
            print(f"{key} : {value}")

    print("\n")

    stats = pull_global_stats(client, thirty_days_since)
    for key, value in stats.items():
        if value:
            print(f"{key} : {value}")


if __name__ == "__main__":
    main()
