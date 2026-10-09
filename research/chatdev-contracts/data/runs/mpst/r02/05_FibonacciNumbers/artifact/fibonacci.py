'''
fibonacci.py
Core logic module for the Fibonacci Number Generator.
Provides:
  * generate_fibonacci_up_to(limit) -- iterative generation of every
    Fibonacci number less than or equal to a given limit.
  * is_fibonacci(number) -- mathematical test (perfect-square check)
    to determine whether a number belongs to the Fibonacci sequence.
'''
import math
def generate_fibonacci_up_to(limit):
    """
    Generate all Fibonacci numbers less than or equal to `limit`.
    The sequence starts with 0 and 1 (i.e. 0, 1, 1, 2, 3, 5, 8, ...).
    Generation stops as soon as the next Fibonacci number would
    exceed the given limit.
    Args:
        limit (int): The inclusive upper bound for generated numbers.
    Returns:
        list[int]: Fibonacci numbers <= limit, in ascending order.
    Raises:
        TypeError: If `limit` is not an integer.
        ValueError: If `limit` is negative.
    """
    if isinstance(limit, bool) or not isinstance(limit, int):
        raise TypeError("limit must be an integer, got: "
                        f"{type(limit).__name__}")
    if limit < 0:
        raise ValueError("limit must be a non-negative integer, "
                         f"got: {limit}")
    sequence = []
    current, nxt = 0, 1
    while current <= limit:
        sequence.append(current)
        current, nxt = nxt, current + nxt
    return sequence
def is_fibonacci(number):
    """
    Check whether a non-negative integer is a Fibonacci number.
    Uses the mathematical property that n is a Fibonacci number if
    and only if (5*n^2 + 4) or (5*n^2 - 4) is a perfect square.
    Args:
        number (int): The number to test.
    Returns:
        bool: True if `number` is a Fibonacci number, False otherwise.
    Raises:
        TypeError: If `number` is not an integer.
    """
    if isinstance(number, bool) or not isinstance(number, int):
        raise TypeError("number must be an integer, got: "
                        f"{type(number).__name__}")
    if number < 0:
        return False
    return (_is_perfect_square(5 * number * number + 4)
            or _is_perfect_square(5 * number * number - 4))
def _is_perfect_square(value):
    """
    Return True if `value` is a perfect square, False otherwise.
    Uses math.isqrt for an exact integer square root, which avoids
    floating-point precision issues with large numbers.
    Args:
        value (int): The value to test.
    Returns:
        bool: True if `value` is a perfect square.
    """
    if value < 0:
        return False
    root = math.isqrt(value)
    return root * root == value