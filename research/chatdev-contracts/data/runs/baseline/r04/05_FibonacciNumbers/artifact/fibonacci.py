'''
fibonacci.py
Core module of the Fibonacci Generator application.
Contains the FibonacciGenerator class, which produces all Fibonacci
numbers up to a user-supplied upper limit. Results are memoized in an
internal cache so repeated queries are fast.
'''
class FibonacciGenerator:
    """Generates Fibonacci numbers up to a given upper limit.
    The sequence starts with 0, 1 and every subsequent number is the sum
    of the two preceding ones. Generated values are cached so that later
    calls with larger limits reuse previously computed numbers.
    """
    def __init__(self):
        """Initialize the generator with the seed values of the sequence."""
        self._cache = [0, 1]
    def generate(self, limit):
        """Return a list of every Fibonacci number that is <= limit.
        Args:
            limit (int): The inclusive upper bound (must be >= 0).
        Returns:
            list[int]: Fibonacci numbers in ascending order, e.g.
                       [0, 1, 1, 2, 3, 5, 8] for limit = 8.
                       Returns an empty list if limit < 0.
        """
        if limit < 0:
            return []
        # Extend the cache until the last value exceeds the limit.
        while self._cache[-1] <= limit:
            self._cache.append(self._cache[-1] + self._cache[-2])
        # Collect every cached value that does not exceed the limit.
        return [number for number in self._cache if number <= limit]
    def count(self, limit):
        """Return how many Fibonacci numbers are <= limit."""
        return len(self.generate(limit))