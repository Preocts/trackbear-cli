"""Main CLI entry point."""

from __future__ import annotations

import cyclopts

# TODO: Create a loader for these (decorator?)
from . import cli_auth


def main() -> int:
    """Main CLI entry point."""
    app = cyclopts.App()

    app.command(cli_auth.commands)

    app()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
