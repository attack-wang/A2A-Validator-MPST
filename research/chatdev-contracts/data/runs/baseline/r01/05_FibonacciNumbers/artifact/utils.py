'''
utils.py
Input parsing and validation helpers shared by the Fibonacci
Generator application.
'''
def parse_limit(raw_value):
    """
    Parse a raw user input string into a non-negative integer limit.
    Args:
        raw_value (str): The raw input supplied by the user.
    Returns:
        int: The parsed non-negative integer.
    Raises:
        ValueError: If the input is empty or not a non-negative integer.
    """
    if raw_value is None:
        raise ValueError("No input provided.")
    cleaned = str(raw_value).strip()
    if not cleaned:
        raise ValueError("Input is empty. Please enter a non-negative integer.")
    try:
        value = int(cleaned)
    except ValueError:
        raise ValueError(f"'{cleaned}' is not a valid integer.")
    if value < 0:
        raise ValueError("The limit must be a non-negative integer.")
    return value
def format_error(message):
    """
    Format an error message with a consistent prefix.
    Args:
        message (str): The raw error message.
    Returns:
        str: The formatted error string.
    """
    return f"[ERROR] {message}"