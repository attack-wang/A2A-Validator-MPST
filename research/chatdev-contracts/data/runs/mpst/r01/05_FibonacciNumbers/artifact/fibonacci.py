'''
fibonacci.py
This module provides the core logic for generating Fibonacci numbers
up to a given limit. It contains the FibonacciGenerator class, which
offers both list-based generation and a memory-efficient generator-based
approach.
'''
class FibonacciGenerator:
    """
    A class responsible for generating Fibonacci numbers up to a given limit.
    """
    def generate(self, limit):
        """
        Generate a list of Fibonacci numbers up to and including the given limit.
        Args:
            limit (int): The maximum value up to which Fibonacci numbers
                         should be generated (inclusive).
        Returns:
            list: A list of Fibonacci numbers less than or equal to the limit.
        Raises:
            ValueError: If the limit is negative.
        """
        if limit < 0:
            raise ValueError("Limit must be a non-negative integer.")
        return list(self.iter_fibonacci(limit))
    def iter_fibonacci(self, limit):
        """
        A generator that yields Fibonacci numbers up to the given limit.
        Args:
            limit (int): The maximum value up to which Fibonacci numbers
                         should be yielded (inclusive).
        Yields:
            int: The next Fibonacci number in the sequence.
        """
        a, b = 0, 1
        while a <= limit:
            yield a
            a, b = b, a + b