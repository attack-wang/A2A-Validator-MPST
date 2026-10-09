'''
utils.py
Utility helpers for input validation and output formatting.
'''
def parse_non_negative_integer(raw_value):
    """
    Parse a raw string into a non-negative integer.
    Args:
        raw_value (str): The raw user input (e.g. from the prompt or argv).
    Returns:
        int: The parsed non-negative integer.
    Raises:
        ValueError: If the input is empty or not a non-negative integer.
    """
    cleaned = str(raw_value).strip()
    if not cleaned:
        raise ValueError("Input cannot be empty.")
    if not cleaned.isdigit():
        raise ValueError("Input must be a non-negative whole number.")
    return int(cleaned)
def format_fibonacci_output(numbers, limit):
    """
    Format the generated Fibonacci numbers as a human-readable summary.
    Args:
        numbers (list[int]): The Fibonacci numbers up to the limit.
        limit (int): The user-provided limit.
    Returns:
        str: A formatted, multi-line summary string.
    """
    header = f"Fibonacci numbers up to {limit} ({len(numbers)} found):"
    body = ", ".join(str(number) for number in numbers)
    return f"{header}\n{body}"