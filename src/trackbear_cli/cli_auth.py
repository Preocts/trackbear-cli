"""CLI routes for Authorization."""

from __future__ import annotations

import cyclopts

from trackbear_cli import auth

commands = cyclopts.App(name="auth")


@commands.command
def save(token: str) -> int:
    """
    Save a TrackBear API token.

    This will be used for all other commands unless overwritten.

    Args:
        token (str): A TrackBear API token.

    Returns:
        int: Value of exit code
    """
    if auth.save(token):
        print(f"Saved the new token ***{token[-4:]}")
        return 0

    print("Failed to save token.")
    return 1


@commands.command
def clear() -> int:
    """
    Clear the stored TrackBear API token.

    Returns:
        int: Value of exit code
    """
    if auth.clear():
        print("The token has been cleared.")
        return 0

    print("Unable to clear token.")
    return 1
