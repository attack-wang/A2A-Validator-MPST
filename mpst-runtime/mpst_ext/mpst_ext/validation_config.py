"""Runtime configuration shared by Host and Remote Agent validators."""

from __future__ import annotations

import os
from typing import Optional


_TRUE_VALUES = {"1", "true", "yes", "on", "enabled"}
_FALSE_VALUES = {"0", "false", "no", "off", "disabled"}


def resolve_validation_enabled(explicit: Optional[bool] = None) -> bool:
    """Resolve the validation switch, defaulting to enabled.

    An explicit constructor argument takes precedence over the environment.
    Invalid environment values fail fast so an experiment cannot silently run
    in the wrong condition.
    """
    if explicit is not None:
        return bool(explicit)

    raw_value = os.getenv("VALIDATION_ENABLED", "true").strip().lower()
    if raw_value in _TRUE_VALUES:
        return True
    if raw_value in _FALSE_VALUES:
        return False
    raise ValueError(
        "VALIDATION_ENABLED must be one of "
        f"{sorted(_TRUE_VALUES | _FALSE_VALUES)}, got {raw_value!r}"
    )
