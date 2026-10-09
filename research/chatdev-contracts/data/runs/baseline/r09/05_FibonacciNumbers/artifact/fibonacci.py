'''
fibonacci.py
This module contains the core logic for generating Fibonacci numbers.
It provides an efficient iterative implementation to generate all
Fibonacci numbers up to a given limit (inclusive), as well as input
validation helpers.
'''
def generate_fibonacci(limit):
    '''
    Generate all Fibonacci numbers up to and including the given limit.
    The sequence starts with 0 and 1, and each subsequent number is
    the sum of the two preceding ones. An efficient iterative approach
    is used, running in O(k) time where k is the count of Fibonacci
    numbers below the limit.
    Args:
        limit (int): The inclusive upper bound for generated numbers.
    Returns:
        list: Fibonacci numbers less than or equal to the limit,
              in ascending order.
    Raises:
        ValueError: If the limit is negative.
    '''
    if limit < 0:
        raise ValueError("Limit must be a non-negative integer.")
    fibonacci_numbers = []
    current, nxt = 0, 1
    while current <= limit:
        fibonacci_numbers.append(current)
        current, nxt = nxt, current + nxt
    return fibonacci_numbers
def validate_limit(raw_value):
    '''
    Validate a raw input string and convert it to a non-negative integer.
    Args:
        raw_value (str): The raw user input to validate.
    Returns:
        int: The validated non-negative integer limit.
    Raises:
        ValueError: If the input is not a valid non-negative integer.
    '''
    try:
        limit = int(str(raw_value).strip())
    except (ValueError, TypeError):
        raise ValueError(f"'{raw_value}' is not a valid integer.")
    if limit < 0:
        raise ValueError("Limit must be a non-negative integer.")
    return limit