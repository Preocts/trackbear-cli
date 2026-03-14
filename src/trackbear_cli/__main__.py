"""Main CLI entry point."""

from __future__ import annotations

import cyclopts

from . import cli_auth


def main(tokens: list[str] | None = None) -> int:
    """Main CLI entry point."""
    app = cyclopts.App()
    # TODO: Create a loader for these
    app.command(cli_auth.commands)

    return app(tokens=tokens, result_action="return_value")


if __name__ == "__main__":
    raise SystemExit(main())
