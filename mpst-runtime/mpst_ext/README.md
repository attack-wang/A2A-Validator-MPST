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
- Incoming and outgoing messages are checked before delivery. A violation
  marks the A2A task as failed and the message is not forwarded.
- Outgoing messages are checked for unexecuted or serialized tool calls before
  protocol-label wrapping. Retriable tool-call failures keep the protocol state
  unchanged and are regenerated in the same agent session (two retries by
  default).
- The A2A adapter adds the currently expected protocol label to ordinary agent
  text, so business agents do not have to manufacture `[label: value]` syntax.
- `finalize()` detects a task or Host workflow that ends before a legal protocol
  completion point.
