"""Manage a stateful configuration."""

from __future__ import annotations

import dataclasses
import enum
import json
import logging
import pathlib

# TODO: We eventually want this to land in the user home directory
_FILEPATH = pathlib.Path.cwd() / "trackbear-cli.json"
_DEFAULT_CONFIG = {
    "auth_token": "",
}

logger = logging.getLogger("trackbear-cli")


class _ConfigFields(str, enum.Enum):
    AUTHTOKEN = "auth_token"


@dataclasses.dataclass(slots=True)
class Config:
    """Manage a stateful configuration."""

    auth_token: str = ""
    fields: type[_ConfigFields] = dataclasses.field(default=_ConfigFields, init=False)

    def __post_init__(self) -> None:
        self._validate_values()

    def _validate_values(self) -> None:
        """Validates all loaded values of the config, raises ValueError when needed."""
        if not isinstance(self.auth_token, str):
            msg = "The TrackBear Auth token must be a string value."
            raise ValueError(msg)

    def load(self) -> None:
        """Load the configuration from disk."""
        if not _FILEPATH.exists():
            logger.info("No configuration found. Creating an empty configuration.")
            json.dump(_DEFAULT_CONFIG, _FILEPATH.open("w", encoding="UTF-8"), indent=2)

        config_dict = json.load(_FILEPATH.open())

        for field in self.fields:
            attr_name = _ConfigFields(field).value
            setattr(self, attr_name, config_dict.get(attr_name, ""))

        self._validate_values()
