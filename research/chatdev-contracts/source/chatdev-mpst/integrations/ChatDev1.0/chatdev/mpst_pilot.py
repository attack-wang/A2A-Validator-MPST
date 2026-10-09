"""Optional, phase-local MPST guard for the legacy ChatDev 1.0 workflow.

This checks each request/response exchange, not the full cross-phase chain.
It reuses the same projected-validator implementation as the ChatDev 2.0
integration while the two workflow architectures remain separate.
"""

from pathlib import Path
from types import SimpleNamespace
import importlib.util
import sys
from typing import Callable


_HERE = Path(__file__).resolve().parents[1]
_CHATDEV_2 = _HERE.parent / "ChatDev"
_MONITOR_SPEC = importlib.util.spec_from_file_location(
    "legacy_chatdev_session_type", _CHATDEV_2 / "session_type.py"
)
_MONITOR_MODULE = importlib.util.module_from_spec(_MONITOR_SPEC)
sys.modules[_MONITOR_SPEC.name] = _MONITOR_MODULE
_MONITOR_SPEC.loader.exec_module(_MONITOR_MODULE)
ChatDevSessionTypeMonitor = _MONITOR_MODULE.ChatDevSessionTypeMonitor


class PhaseExchangeMonitor:
    def __init__(self):
        self.monitor = ChatDevSessionTypeMonitor(
            protocol_path=_HERE / "protocol" / "mpst_phase_exchange.gt",
            role_map={"requester": "Requester", "responder": "Responder"},
            use_default_roles=False,
            max_retries=2,
        )
        self.requester = SimpleNamespace(id="requester")
        self.responder = SimpleNamespace(id="responder")

    def snapshot(self):
        return self.monitor.snapshot_state()

    def restore(self, snapshot):
        self.monitor.restore_state(snapshot)

    def request(self, message):
        return self.monitor.check(
            SimpleNamespace(target=self.responder), message, self.requester
        )

    def response(self, message):
        return self.monitor.check(
            SimpleNamespace(target=self.requester), message, self.responder
        )

    @property
    def complete(self):
        return self.monitor.is_terminated


def run_checked_exchange(
    initial_message,
    generate: Callable,
    feedback_factory: Callable,
    max_retries: int,
    phase_name: str,
    on_retry: Callable = lambda attempt: None,
    exchange_factory: Callable = PhaseExchangeMonitor,
):
    """Validate one exchange, rolling back protocol state on an empty reply."""
    if max_retries < 0:
        raise ValueError("max_retries must be non-negative")
    exchange = exchange_factory()
    message = initial_message
    for attempt in range(max_retries + 1):
        checkpoint = exchange.snapshot()
        exchange.request(message)
        assistant_response, user_response = generate(message)
        reply = assistant_response.msg
        if reply is not None and str(getattr(reply, "content", "") or "").strip():
            exchange.response(reply)
            if not exchange.complete:
                raise RuntimeError("MPST exchange did not terminate")
            return assistant_response, user_response, attempt
        exchange.restore(checkpoint)
        if attempt >= max_retries:
            raise RuntimeError(
                "MPST pilot rejected an empty response after {} retries in {}".format(
                    max_retries, phase_name
                )
            )
        on_retry(attempt + 1)
        message = feedback_factory(message, attempt + 1)
    raise AssertionError("unreachable")
