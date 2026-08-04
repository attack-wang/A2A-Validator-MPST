"""Readable validation-error logging for the Host process."""

from __future__ import annotations

import json
import logging

from typing import Any


logger = logging.getLogger('host.validation')


def _preview(content: Any, limit: int = 500) -> str:
    if content is None:
        return ''
    if isinstance(content, str):
        text = content
    else:
        try:
            text = json.dumps(content, ensure_ascii=False, default=str)
        except (TypeError, ValueError):
            text = str(content)
    text = text.replace('\r', '\\r').replace('\n', '\\n')
    if len(text) > limit:
        return f'{text[:limit]}...'
    return text


def log_host_validation_error(
    *,
    stage: str,
    code: str | None,
    error: str | None,
    session_id: str | None = None,
    peer: str | None = None,
    position: str | None = None,
    expected: Any = None,
    content: Any = None,
    action: str | None = None,
) -> None:
    """Write one consistent, multiline Host validation-error entry."""
    logger.error(
        '[HOST VALIDATION ERROR]\n'
        '  Stage: %s\n'
        '  Code: %s\n'
        '  Error: %s\n'
        '  Session: %s\n'
        '  Peer: %s\n'
        '  Current position: %s\n'
        '  Expected transitions: %s\n'
        '  Content: %s\n'
        '  Action: %s',
        stage,
        code or 'Unknown',
        error or 'Unknown validation error',
        session_id or 'N/A',
        peer or 'N/A',
        position or 'N/A',
        _preview(expected) or 'N/A',
        _preview(content) or 'N/A',
        action or 'rejected',
    )
