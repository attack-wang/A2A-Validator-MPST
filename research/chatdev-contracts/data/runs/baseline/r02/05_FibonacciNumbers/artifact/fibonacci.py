'''
fibonacci.py
Core logic of the Fibonacci Generator application.
This module is responsible for producing Fibonacci numbers up to a
given upper limit. It offers:
    * `fibonacci_generator`      - a memory-efficient generator that
                                   yields Fibonacci numbers one by one.
    * `generate_fibonacci_up_to` - returns all Fibonacci numbers up to
                                   a limit as a plain list.
    * `is_fibonacci`             - checks whether a given integer is a
                                   Fibonacci number.
The sequence used here starts with 0 and 1, i.e. 0, 1, 1, 2, 3, 5, 8, ...
'''
import math
def fibonacci_generator(limit):
    """
    Yield every Fibonacci number that does not exceed `limit`.
    The generator keeps only the last two values in memory, so it works
    efficiently even for very large limits.
    Args:
        limit (int): Non-negative upper bound (inclusive).
    Yields:
        int: The next Fibonacci number <= limit, in ascending order.
    """
    previous, current = 0, 1
    while previous <= limit:
        yield previous
        previous, current = current, previous + current
def generate_fibonacci_up_to(limit):
    """
    Collect every Fibonacci number up to (and including) `limit`.
    Args:
        limit (int): Non-negative upper bound (inclusive).
    Returns:
        list[int]: Ascending list of Fibonacci numbers <= limit.
                   Example: limit=10 -> [0, 1, 1, 2, 3, 5, 8]
    """
    return list(fibonacci_generator(limit))
def _is_perfect_square(value):
    """
    Return True if `value` is a perfect square.
    Uses math.isqrt, which is exact for arbitrarily large integers.
    Args:
        value (int): The number to test.
    Returns:
        bool: True if `value` is a perfect square, otherwise False.
    """
    if value < 0:
        return False
    root = math.isqrt(value)
    return root * root == value
def is_fibonacci(number):
    """
    Check whether `number` is a Fibonacci number.
    A non-negative integer n is a Fibonacci number if and only if
    5*n^2 + 4 or 5*n^2 - 4 is a perfect square.
    Args:
        number (int): The number to check.
    Returns:
        bool: True if `number` is a Fibonacci number, otherwise False.
    """
    if number < 0:
        return False
    return (
        _is_perfect_square(5 * number * number + 4)
        or _is_perfect_square(5 * number * number - 4)
    )