'''
fibonacci.py
Core Fibonacci generation logic. Provides:
  * generate_fibonacci(limit)  -> list of Fibonacci numbers <= limit
  * fibonacci_generator(limit) -> lazy generator of the same sequence
  * is_fibonacci_number(n)     -> membership test for a single integer
'''
import math
def generate_fibonacci(limit):
    '''
    Generate all Fibonacci numbers up to and including `limit`.
    The sequence starts 0, 1, 1, 2, 3, 5, ... and every value that is
    less than or equal to `limit` is collected.
    Args:
        limit (int): Inclusive upper bound for the generated numbers.
    Returns:
        list[int]: Fibonacci numbers <= limit in ascending order.
                   Returns [0] for limit == 0 and [] for limit < 0.
    '''
    result = []
    a, b = 0, 1
    while a <= limit:
        result.append(a)
        a, b = b, a + b
    return result
def fibonacci_generator(limit):
    '''
    Lazily yield Fibonacci numbers up to and including `limit`.
    The sequence starts 0, 1, 1, 2, 3, 5, ... and every value that is
    less than or equal to `limit` is produced one at a time, so the
    caller never materializes the whole list in memory.
    Args:
        limit (int): Inclusive upper bound for the generated numbers.
    Yields:
        int: The next Fibonacci number <= limit in ascending order.
    '''
    a, b = 0, 1
    while a <= limit:
        yield a
        a, b = b, a + b
def _is_perfect_square(x):
    '''
    Return True if `x` is a perfect square, else False.
    Args:
        x (int): Candidate integer.
    Returns:
        bool: True when there exists an integer r with r*r == x.
    '''
    if x < 0:
        return False
    root = math.isqrt(x)
    return root * root == x
def is_fibonacci_number(n):
    '''
    Test whether a single integer is a Fibonacci number.
    Uses the classical perfect-square characterization: n is a
    Fibonacci number if and only if 5*n^2 + 4 or 5*n^2 - 4 is a
    perfect square.
    Args:
        n (int): Candidate integer.
    Returns:
        bool: True if n appears in the Fibonacci sequence, else False.
    '''
    if n < 0:
        return False
    return _is_perfect_square(5 * n * n + 4) or _is_perfect_square(5 * n * n - 4)