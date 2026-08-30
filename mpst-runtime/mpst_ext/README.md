# mpst_ext

MPST (Multiparty Session Types) validation extension for A2A agents.

Provides `MPSTValidator`, `MPSTValidationExtension`, and `MPSTValidatingExecutor`
for runtime protocol validation across A2A agent interactions.

Runtime enforcement is enabled by default. Set
`VALIDATION_ENABLED=false` before starting every Host and Remote Agent process
to use the unvalidated pass-through path for a controlled baseline experiment.

## Runtime behavior

- Local types and subset-projection FSM output are compiled into a shared
  protocol automaton with sequencing, choice, recursion, and terminal states.
- Validator state is isolated by A2A context/session; protocol templates are
  shared, execution positions are not.
- Incoming and outgoing messages are checked before delivery. Rejected output
  is never forwarded and never advances the protocol state.
- Outgoing messages are checked for unexecuted or serialized tool calls before
  protocol-label wrapping. Recoverable tool-call, label, and value-type errors
  are converted into structured model feedback containing the error code,
  reason, protocol position, and expected transitions. The agent regenerates in
  the same session (two retries by default); exhaustion still fails closed.
- The A2A adapter adds the currently expected protocol label to ordinary agent
  text, so business agents do not have to manufacture `[label: value]` syntax.
- `finalize()` detects a task or Host workflow that ends before a legal protocol
  completion point.

## Error-feedback recovery

- `MPST_ERROR_FEEDBACK_ENABLED=true` enables corrective regeneration (default).
- `MPST_ERROR_FEEDBACK_ENABLED=false` keeps validation enabled but fails on the
  first rejected model output.
- `MPST_ERROR_FEEDBACK_MAX_RETRIES=2` sets the maximum correction attempts;
  `0` disables retries while preserving validation.
- Constructor arguments `error_feedback_enabled` and `max_validation_retries`
  override the environment for an individual executor.
