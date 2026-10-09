'''
io_utils.py
This module provides safe input handling for the Connect Four
application. The safe_input helper wraps the built-in input()
function so that a closed or exhausted standard input stream
(EOFError) or a user interrupt (KeyboardInterrupt) is reported as
None instead of crashing the program. The InputClosed exception is
raised by callers that cannot proceed without input, allowing the
application to shut down gracefully in non-interactive environments
such as automated test harnesses or piped-input runs.
'''
class InputClosed(Exception):
    """Raised when user input is required but stdin is unavailable."""
    pass
def safe_input(prompt: str):
    """
    Read one line from standard input without ever raising EOFError
    or KeyboardInterrupt.
    Args:
        prompt: Text displayed to the user before reading.
    Returns:
        The raw input string, or None when the input stream is
        closed or interrupted.
    """
    try:
        return input(prompt)
    except EOFError:
        return None
    except KeyboardInterrupt:
        return None