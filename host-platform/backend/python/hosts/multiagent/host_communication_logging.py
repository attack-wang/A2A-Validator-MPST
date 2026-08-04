"""Structured application-level trace of Host-to-Agent A2A communication."""

from __future__ import annotations

import json
import logging
import time

from typing import Any


logger = logging.getLogger('host.communication')


def _serializable(value: Any) -> Any:
    if hasattr(value, 'model_dump'):
        return value.model_dump(mode='json')
    return value


def log_a2a_communication(  # noqa: PLR0913
    *,
    direction: str,
    phase: str,
    peer: str,
    context_id: str | None,
    task_id: str | None,
    message_id: str | None,
    payload: Any,
) -> None:
    """Write one machine-readable trace record without changing message flow."""
    record = {
        'timestamp': time.time(),
        'direction': direction,
        'phase': phase,
        'peer': peer,
        'context_id': context_id,
        'task_id': task_id,
        'message_id': message_id,
        'payload': _serializable(payload),
    }
    logger.info(
        '[A2A COMMUNICATION] %s',
        json.dumps(record, ensure_ascii=False, default=str),
    )
