'''
fibonacci.py
Core module containing the Fibonacci number generation logic.
Provides:
    * generate_fibonacci_up_to(limit)  -> list of Fibonacci numbers <= limit
    * fibonacci_generator(limit)       -> lazy generator of Fibonacci numbers <= limit
    * is_fibonacci_number(n)           -> test whether n is a Fibonacci number
The sequence starts at 0: 0, 1, 1, 2, 3, 5, 8, 13, ...
'''
import math
def _validate_limit(limit):
    '''
    Validate that a limit is a non-negative integer.
    Args:
        limit (int): The value to validate.
    Raises:
        TypeError: If limit is not an integer.
        ValueError: If limit is negative.
    '''
    if isinstance(limit, bool) or not isinstance(limit, int):
        raise TypeError(f"limit must be an integer, got {type(limit).__name__}")
    if limit < 0:
        raise ValueError(f"limit must be non-negative, got {limit}")
def generate_fibonacci_up_to(limit):
    '''
    Generate all Fibonacci numbers up to and including the given limit.
    Args:
        limit (int): The inclusive upper bound for generated Fibonacci numbers.
    Returns:
        list[int]: Every Fibonacci number n such that n <= limit, in ascending order.
    Raises:
        TypeError: If limit is not an integer.
        ValueError: If limit is negative.
    Examples:
        >>> generate_fibonacci_up_to(10)
        [0, 1, 1, 2, 3, 5, 8]
        >>> generate_fibonacci_up_to(0)
        [0]
    '''
    _validate_limit(limit)
    sequence = []
    a, b = 0, 1
    while a <= limit:
        sequence.append(a)
        a, b = b, a + b
    return sequence
def fibonacci_generator(limit):
    '''
    Lazily yield Fibonacci numbers up to and including the given limit.
    Memory efficient: numbers are produced one at a time instead of being
    stored in a list, which is useful for very large limits.
    Args:
        limit (int): The inclusive upper bound for generated Fibonacci numbers.
    Yields:
        int: The next Fibonacci number that is <= limit.
    Raises:
        TypeError: If limit is not an integer.
        ValueError: If limit is negative.
    Examples:
        >>> list(fibonacci_generator(20))
        [0, 1, 1, 2, 3, 5, 8, 13]
    '''
    _validate_limit(limit)
    a, b = 0, 1
    while a <= limit:
        yield a
        a, b = b, a + b
def is_fibonacci_number(n):
    '''
    Check whether a given integer is a Fibonacci number.
    Uses the mathematical property that n >= 0 is a Fibonacci number if and
    only if (5 * n^2 + 4) or (5 * n^2 - 4) is a perfect square.
    Args:
        n (int): The number to test.
    Returns:
        bool: True if n is a Fibonacci number, False otherwise.
    Raises:
        TypeError: If n is not an integer.
    Examples:
        >>> is_fibonacci_number(8)
        True
        >>> is_fibonacci_number(9)
        False
    '''
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be an integer, got {type(n).__name__}")
    if n < 0:
        return False
    def _is_perfect_square(value):
        if value < 0:
            return False
        root = math.isqrt(value)
        return root * root == value
    candidate = 5 * n * n
    return _is_perfect_square(candidate + 4) or _is_perfect_square(candidate - 4)