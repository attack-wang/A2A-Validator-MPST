'''
fibonacci.py
Core module for generating Fibonacci numbers up to a given limit.
This module provides:
- validate_limit: validates and converts raw user input into a non-negative integer.
- fibonacci_generator: a memory-efficient generator yielding Fibonacci numbers <= limit.
- generate_fibonacci_up_to: returns a list of all Fibonacci numbers <= limit.
The sequence produced is 0, 1, 1, 2, 3, 5, 8, 13, 21, ...
'''
def validate_limit(raw_value):
    """
    Validate and convert a raw input string into a non-negative integer.
    Args:
        raw_value: The raw user input (typically a string).
    Returns:
        int: The validated non-negative integer limit.
    Raises:
        ValueError: If the input is not a valid integer or is negative.
    """
    try:
        value = int(str(raw_value).strip())
    except (TypeError, ValueError):
        raise ValueError(f"'{raw_value}' is not a valid integer.")
    if value < 0:
        raise ValueError("The limit must be a non-negative integer.")
    return value
def fibonacci_generator(limit):
    """
    Yield Fibonacci numbers one at a time, up to and including the limit.
    The sequence starts at 0, 1, 1, 2, 3, 5, ... and stops once the next
    number would exceed the given limit. Being a generator, it uses O(1)
    memory regardless of how many numbers are produced.
    Args:
        limit (int): The maximum Fibonacci number to generate (inclusive).
    Yields:
        int: The next Fibonacci number that is <= limit.
    """
    current, nxt = 0, 1
    while current <= limit:
        yield current
        current, nxt = nxt, current + nxt
def generate_fibonacci_up_to(limit):
    """
    Generate all Fibonacci numbers up to and including the given limit.
    Args:
        limit (int): The maximum Fibonacci number to generate (inclusive).
    Returns:
        list: A list of all Fibonacci numbers <= limit, in ascending order.
    Examples:
        >>> generate_fibonacci_up_to(10)
        [0, 1, 1, 2, 3, 5, 8]
        >>> generate_fibonacci_up_to(0)
        [0]
    """
    return list(fibonacci_generator(limit))