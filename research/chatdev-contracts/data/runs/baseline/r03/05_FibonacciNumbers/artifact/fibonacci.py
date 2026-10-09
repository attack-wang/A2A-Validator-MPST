'''
fibonacci.py
Core logic for validating user input and generating Fibonacci numbers.
'''
import re
def validate_limit(raw_limit: str) -> int:
    """
    Validate raw user input and convert it to a non-negative integer.
    Args:
        raw_limit: Raw user input, e.g. "100".
    Returns:
        The validated limit as a non-negative integer.
    Raises:
        ValueError: If the input is not a valid non-negative integer.
    """
    raw = str(raw_limit).strip()
    if not raw:
        raise ValueError("Input is empty. Please enter a non-negative integer.")
    if not re.fullmatch(r"\d+", raw):
        raise ValueError(f"'{raw}' is not a valid non-negative integer.")
    return int(raw)
def generate_fibonacci_up_to(limit: int) -> list:
    """
    Generate all Fibonacci numbers less than or equal to the given limit.
    The sequence starts at 0 (i.e., 0, 1, 1, 2, 3, 5, ...).
    Args:
        limit: Inclusive upper bound (non-negative integer).
    Returns:
        A list of Fibonacci numbers up to and including the limit.
        Example: limit=10 -> [0, 1, 1, 2, 3, 5, 8]
    """
    if limit < 0:
        raise ValueError("Limit must be non-negative.")
    numbers = []
    a, b = 0, 1
    while a <= limit:
        numbers.append(a)
        a, b = b, a + b
    return numbers