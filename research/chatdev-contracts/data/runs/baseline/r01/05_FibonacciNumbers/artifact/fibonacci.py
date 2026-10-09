'''
fibonacci.py
Core logic for generating Fibonacci numbers up to a given limit.
Provides a list-based implementation, a memory-efficient generator,
and a membership test for Fibonacci numbers.
Note: requires Python >= 3.8 (uses math.isqrt).
'''
import math
def _validate_limit(limit):
    """Raise an error if limit is not a non-negative integer."""
    if not isinstance(limit, int) or isinstance(limit, bool):
        raise TypeError("Limit must be an integer.")
    if limit < 0:
        raise ValueError("Limit must be a non-negative integer.")
def generate_fibonacci(limit):
    """
    Generate all Fibonacci numbers up to and including the given limit.
    Args:
        limit (int): Maximum value (inclusive) for generated numbers.
    Returns:
        list[int]: Fibonacci numbers, each <= limit, in ascending order.
    """
    _validate_limit(limit)
    sequence = []
    a, b = 0, 1
    while a <= limit:
        sequence.append(a)
        a, b = b, a + b
    return sequence
def fibonacci_generator(limit):
    """
    Lazily yield Fibonacci numbers up to the given limit.
    Args:
        limit (int): Maximum value (inclusive) for generated numbers.
    Yields:
        int: The next Fibonacci number that is <= limit.
    """
    _validate_limit(limit)
    a, b = 0, 1
    while a <= limit:
        yield a
        a, b = b, a + b
def is_fibonacci(n):
    """
    Check whether a non-negative integer is a Fibonacci number.
    Uses the mathematical property that x is a Fibonacci number iff
    (5*x^2 + 4) or (5*x^2 - 4) is a perfect square.
    Args:
        n (int): The number to test.
    Returns:
        bool: True if n is a Fibonacci number, False otherwise.
    """
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("Input must be an integer.")
    if n < 0:
        return False
    def _is_perfect_square(value):
        if value < 0:
            return False
        root = math.isqrt(value)
        return root * root == value
    return _is_perfect_square(5 * n * n + 4) or _is_perfect_square(5 * n * n - 4)