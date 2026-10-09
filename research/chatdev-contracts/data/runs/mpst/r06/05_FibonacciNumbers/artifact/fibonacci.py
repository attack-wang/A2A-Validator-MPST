'''
fibonacci.py
Core logic module for the Fibonacci Generator application.
Provides the FibonacciGenerator class, which generates all Fibonacci
numbers up to a given limit (inclusive), as well as the first N
Fibonacci numbers on demand.
'''
class FibonacciGenerator:
    '''
    Generates Fibonacci numbers.
    The Fibonacci sequence starts with 0 and 1, and every subsequent
    number is the sum of the two preceding ones:
        0, 1, 1, 2, 3, 5, 8, 13, 21, 34, ...
    '''
    def __init__(self):
        '''Initialize the generator with an empty history.'''
        self._last_sequence = []
    def generate(self, limit):
        '''
        Generate all Fibonacci numbers up to and including `limit`.
        Args:
            limit (int): The inclusive upper bound for generated numbers.
        Returns:
            list[int]: Fibonacci numbers that are <= limit.
        Raises:
            ValueError: If `limit` is negative.
        '''
        if limit < 0:
            raise ValueError("Limit must be a non-negative integer.")
        sequence = []
        a, b = 0, 1
        while a <= limit:
            sequence.append(a)
            a, b = b, a + b
        self._last_sequence = sequence
        return sequence
    def generate_count(self, count):
        '''
        Generate the first `count` Fibonacci numbers.
        Args:
            count (int): How many Fibonacci numbers to generate.
        Returns:
            list[int]: The first `count` Fibonacci numbers.
        Raises:
            ValueError: If `count` is negative.
        '''
        if count < 0:
            raise ValueError("Count must be a non-negative integer.")
        sequence = []
        a, b = 0, 1
        for _ in range(count):
            sequence.append(a)
            a, b = b, a + b
        self._last_sequence = sequence
        return sequence
    @property
    def last_sequence(self):
        '''Return the most recently generated Fibonacci sequence.'''
        return self._last_sequence