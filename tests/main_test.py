from __future__ import annotations

import pytest

from trackbear_cli import __main__ as main


def test_main(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the primary entry of the CLI."""
    expected_start = "Usage:"

    main.main(["--help"])
    output = capsys.readouterr()

    assert output.out.startswith(expected_start)


def test_main_error(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the primary entry of the CLI."""
    with pytest.raises(SystemExit):
        main.main(["invalid command"])
