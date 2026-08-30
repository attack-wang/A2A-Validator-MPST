"""Runtime configuration shared by Host and Remote Agent validators."""

from __future__ import annotations

import os
from typing import Optional


_TRUE_VALUES = {"1", "true", "yes", "on", "enabled"}
_FALSE_VALUES = {"0", "false", "no", "off", "disabled"}


def _resolve_bool_setting(
    name: str,
    explicit: Optional[bool],
    *,
    default: bool,
) -> bool:
    if explicit is not None:
        return bool(explicit)

    raw_value = os.getenv(name, str(default).lower()).strip().lower()
    if raw_value in _TRUE_VALUES:
        return True
    if raw_value in _FALSE_VALUES:
        return False
    raise ValueError(
        f"{name} must be one of "
        f"{sorted(_TRUE_VALUES | _FALSE_VALUES)}, got {raw_value!r}"
    )


def resolve_validation_enabled(explicit: Optional[bool] = None) -> bool:
    """Resolve the validation switch, defaulting to enabled.

    An explicit constructor argument takes precedence over the environment.
    Invalid environment values fail fast so an experiment cannot silently run
    in the wrong condition.
    """
    return _resolve_bool_setting(
        "VALIDATION_ENABLED",
        explicit,
        default=True,
    )


def resolve_error_feedback_enabled(explicit: Optional[bool] = None) -> bool:
    """Resolve whether rejected model output is fed back for regeneration."""
    return _resolve_bool_setting(
        "MPST_ERROR_FEEDBACK_ENABLED",
        explicit,
        default=True,
    )


def resolve_error_feedback_max_retries(
    explicit: Optional[int] = None,
    *,
    default: int = 2,
) -> int:
    """Resolve the bounded number of model correction attempts."""
    raw_value: object = explicit
    if raw_value is None:
        raw_value = os.getenv("MPST_ERROR_FEEDBACK_MAX_RETRIES", str(default))
    try:
        retries = int(str(raw_value).strip())
    except (TypeError, ValueError) as exc:
        raise ValueError(
            "MPST_ERROR_FEEDBACK_MAX_RETRIES must be a non-negative integer, "
            f"got {raw_value!r}"
        ) from exc
    if retries < 0:
        raise ValueError(
            "MPST_ERROR_FEEDBACK_MAX_RETRIES must be a non-negative integer, "
            f"got {raw_value!r}"
        )
    return retries
