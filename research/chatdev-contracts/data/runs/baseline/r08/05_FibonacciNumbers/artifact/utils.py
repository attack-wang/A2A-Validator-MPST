'''
utils.py
Utility helpers for input parsing and validation shared across the
Fibonacci generator application.
'''
class InputValidationError(ValueError):
    '''
    Exception raised when user input cannot be interpreted as a valid
    non-negative integer limit.
    '''
    pass
def parse_integer(text):
    '''
    Convert raw text into an integer.
    Args:
        text (str): Raw input text, e.g. from the command line or stdin.
    Returns:
        int: The parsed integer value.
    Raises:
        InputValidationError: If `text` is empty or not a valid integer.
    '''
    stripped = str(text).strip()
    if not stripped:
        raise InputValidationError("Input is empty; please enter an integer.")
    try:
        return int(stripped)
    except ValueError:
        raise InputValidationError(f"'{stripped}' is not a valid integer.")
def validate_limit(value):
    '''
    Ensure a value is a non-negative integer usable as a Fibonacci limit.
    Args:
        value (int): Candidate limit value.
    Returns:
        int: The validated limit (unchanged).
    Raises:
        InputValidationError: If `value` is negative.
    '''
    if value < 0:
        raise InputValidationError(
            "The limit must be a non-negative integer (got {}).".format(value)
        )
    return value