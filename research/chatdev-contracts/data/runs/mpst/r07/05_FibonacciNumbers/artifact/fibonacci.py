'''
fibonacci.py
Core Fibonacci generation logic for the Fibonacci Number Generator.
Provides:
- fibonacci_generator: memory-efficient generator yielding Fibonacci
  numbers up to an inclusive limit.
- generate_fibonacci_up_to: convenience wrapper returning the full list.
- is_fibonacci: membership test based on the perfect-square property.
- parse_limit: validation/conversion of raw user input into a limit.
'''
import math
from typing import Generator, List
def fibonacci_generator(limit: int) -> Generator[int, None, None]:
    """
    Yield every Fibonacci number less than or equal to ``limit``.
    The sequence starts 0, 1, 1, 2, 3, 5, 8, ... and stops as soon as the
    next term would exceed ``limit``. Because values are produced lazily,
    the generator works efficiently even for very large limits.
    Parameters
    ----------
    limit : int
        Inclusive upper bound. Must be a non-negative integer.
    Yields
    ------
    int
        The next Fibonacci number not exceeding ``limit``.
    Raises
    ------
    ValueError
        If ``limit`` is negative.
    """
    if limit < 0:
        raise ValueError("The limit must be a non-negative integer.")
    current, nxt = 0, 1
    while current <= limit:
        yield current
        current, nxt = nxt, current + nxt
def generate_fibonacci_up_to(limit: int) -> List[int]:
    """
    Return the list of all Fibonacci numbers less than or equal to ``limit``.
    Parameters
    ----------
    limit : int
        Inclusive upper bound (non-negative integer).
    Returns
    -------
    List[int]
        Fibonacci numbers in ascending order, e.g. for limit=10:
        [0, 1, 1, 2, 3, 5, 8].
    Raises
    ------
    ValueError
        If ``limit`` is negative.
    """
    return list(fibonacci_generator(limit))
def _is_perfect_square(value: int) -> bool:
    """
    Return True if ``value`` is a perfect square.
    Uses ``math.isqrt`` so the check is exact for arbitrarily large
    integers (no floating-point rounding issues).
    """
    if value < 0:
        return False
    root = math.isqrt(value)
    return root * root == value
def is_fibonacci(n: int) -> bool:
    """
    Check whether ``n`` is a Fibonacci number.
    A non-negative integer x is a Fibonacci number if and only if one of
    5*x^2 + 4 or 5*x^2 - 4 is a perfect square.
    Parameters
    ----------
    n : int
        The number to test.
    Returns
    -------
    bool
        True when ``n`` is a Fibonacci number, False otherwise.
    """
    if n < 0:
        return False
    return _is_perfect_square(5 * n * n + 4) or _is_perfect_square(5 * n * n - 4)
def parse_limit(raw: str) -> int:
    """
    Convert raw user input into a validated non-negative integer limit.
    Parameters
    ----------
    raw : str
        Raw input string, e.g. from the command line or an interactive
        prompt.
    Returns
    -------
    int
        The parsed non-negative integer limit.
    Raises
    ------
    ValueError
        If the input is empty, not an integer, or negative.
    """
    text = raw.strip()
    if not text:
        raise ValueError("Input is empty; please enter a non-negative integer.")
    try:
        value = int(text)
    except ValueError:
        raise ValueError(f"'{text}' is not a valid integer.")
    if value < 0:
        raise ValueError(f"The limit must be non-negative (got {value}).")
    return value