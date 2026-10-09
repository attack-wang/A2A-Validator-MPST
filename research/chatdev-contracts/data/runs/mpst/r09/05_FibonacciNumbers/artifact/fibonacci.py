'''
fibonacci.py
Core module containing the Fibonacci number generation logic.
Provides:
  - a memory-efficient generator that streams Fibonacci numbers up to a limit,
  - a list-based API for easy display and testing,
  - a count-based API for the first N Fibonacci numbers,
  - a class-based interface that caches the most recent sequence.
'''
def generate_fibonacci(limit):
    """
    Generator that yields Fibonacci numbers up to and including `limit`.
    Uses an iterative two-variable approach: O(n) time, O(1) extra space.
    Args:
        limit (int): The upper bound (inclusive) for generated numbers.
    Yields:
        int: The next Fibonacci number not exceeding `limit`.
    """
    a, b = 0, 1
    while a <= limit:
        yield a
        a, b = b, a + b
def fibonacci_list(limit):
    """
    Return a list of all Fibonacci numbers up to and including `limit`.
    Args:
        limit (int): The upper bound (inclusive).
    Returns:
        list[int]: Fibonacci numbers <= limit, in ascending order.
                   Returns an empty list if limit is negative.
    """
    return list(generate_fibonacci(limit))
def fibonacci_up_to_count(count):
    """
    Return a list of the first `count` Fibonacci numbers.
    Args:
        count (int): How many Fibonacci numbers to produce (must be >= 0).
    Returns:
        list[int]: The first `count` Fibonacci numbers, starting at 0.
    Raises:
        ValueError: If count is negative.
    """
    if count < 0:
        raise ValueError("count must be a non-negative integer")
    result = []
    a, b = 0, 1
    for _ in range(count):
        result.append(a)
        a, b = b, a + b
    return result
class FibonacciGenerator:
    """
    Class-based wrapper around the Fibonacci generation logic.
    Caches the most recently generated sequence so it can be re-displayed
    or exported without recomputation.
    """
    def __init__(self, limit=0):
        """
        Initialize the generator with an upper bound.
        Args:
            limit (int): The upper bound (inclusive) for Fibonacci numbers.
        """
        self.limit = limit
        self._sequence = []
    def set_limit(self, limit):
        """
        Update the upper bound and clear any cached sequence.
        Args:
            limit (int): New upper bound (inclusive).
        """
        self.limit = limit
        self._sequence = []
    def generate(self):
        """
        Generate the Fibonacci sequence up to the current limit and cache it.
        Returns:
            list[int]: Fibonacci numbers <= the current limit.
        """
        self._sequence = fibonacci_list(self.limit)
        return self._sequence
    @property
    def last_sequence(self):
        """
        Return the most recently generated sequence (empty if none yet).
        """
        return self._sequence