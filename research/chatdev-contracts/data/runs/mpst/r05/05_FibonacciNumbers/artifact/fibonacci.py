'''
Module: fibonacci.py
This module contains the core logic for generating Fibonacci numbers
up to a given limit. It provides a FibonacciGenerator class that
encapsulates the generation algorithm, as well as a convenience
function generate_fibonacci() for quick one-call usage.
'''
class FibonacciGenerator:
    """
    Generates the Fibonacci sequence up to (and including) a given limit.
    The Fibonacci sequence starts with 0 and 1, and every subsequent
    number is the sum of the two preceding ones:
        0, 1, 1, 2, 3, 5, 8, 13, 21, ...
    """
    def __init__(self, limit):
        """
        Initialize the generator.
        Args:
            limit (int): The upper bound (inclusive) for generated numbers.
        Raises:
            TypeError: If limit is not an integer.
            ValueError: If limit is negative.
        """
        if isinstance(limit, bool) or not isinstance(limit, int):
            raise TypeError("Limit must be an integer.")
        if limit < 0:
            raise ValueError("Limit must be a non-negative integer.")
        self.limit = limit
    def generate(self):
        """
        Generate all Fibonacci numbers up to and including self.limit.
        Uses an iterative O(n) algorithm with O(1) auxiliary space.
        Returns:
            list[int]: The Fibonacci sequence up to the limit.
        """
        sequence = []
        a, b = 0, 1
        while a <= self.limit:
            sequence.append(a)
            a, b = b, a + b
        return sequence
    def __iter__(self):
        """Allow iteration over the generated Fibonacci numbers."""
        return iter(self.generate())
    def __len__(self):
        """Return how many Fibonacci numbers exist up to the limit."""
        return len(self.generate())
    def __str__(self):
        """Return a human-readable description of the generator."""
        return f"FibonacciGenerator(limit={self.limit})"
def generate_fibonacci(limit):
    """
    Convenience function: generate Fibonacci numbers up to a limit.
    Args:
        limit (int): The upper bound (inclusive).
    Returns:
        list[int]: The Fibonacci sequence up to the limit.
    """
    return FibonacciGenerator(limit).generate()