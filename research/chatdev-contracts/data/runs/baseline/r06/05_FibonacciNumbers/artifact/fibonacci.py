'''
fibonacci.py
Core module containing the Fibonacci number generation logic.
'''
import math
def generate_fibonacci_up_to(limit):
    """
    Generate all Fibonacci numbers up to and including the given limit.
    The sequence starts at 0, 1, 1, 2, 3, 5, ...
    Args:
        limit (int): The inclusive upper bound for generated numbers.
    Returns:
        list[int]: All Fibonacci numbers less than or equal to the limit.
    Raises:
        ValueError: If the limit is negative.
    """
    if limit < 0:
        raise ValueError("Limit must be a non-negative integer.")
    fibonacci_numbers = []
    a, b = 0, 1
    while a <= limit:
        fibonacci_numbers.append(a)
        a, b = b, a + b
    return fibonacci_numbers
def fibonacci_generator(limit):
    """
    Lazily yield Fibonacci numbers up to and including the given limit.
    Useful for very large limits because numbers are produced one at a
    time instead of being stored in a list.
    Args:
        limit (int): The inclusive upper bound.
    Yields:
        int: The next Fibonacci number that is <= limit.
    Raises:
        ValueError: If the limit is negative (raised on first iteration).
    """
    if limit < 0:
        raise ValueError("Limit must be a non-negative integer.")
    a, b = 0, 1
    while a <= limit:
        yield a
        a, b = b, a + b
def is_fibonacci_number(n):
    """
    Check whether a non-negative integer is a Fibonacci number.
    Uses the mathematical property that n is a Fibonacci number if and
    only if (5 * n^2 + 4) or (5 * n^2 - 4) is a perfect square.
    Args:
        n (int): The number to test.
    Returns:
        bool: True if n is a Fibonacci number, False otherwise.
    """
    if n < 0:
        return False
    def is_perfect_square(value):
        """Return True if value is a perfect square."""
        if value < 0:
            return False
        root = math.isqrt(value)
        return root * root == value
    return is_perfect_square(5 * n * n + 4) or is_perfect_square(5 * n * n - 4)