'''
fibonacci.py
Core logic module for generating Fibonacci numbers up to a given limit.
Provides both a class-based generator (FibonacciGenerator) supporting
eager generation and lazy iteration, and a simple functional interface
(generate_fibonacci_up_to).
'''
class FibonacciGenerator:
    '''
    A class that generates Fibonacci numbers up to a given limit.
    Attributes:
        limit (int): The maximum value (inclusive) a Fibonacci number may reach.
    '''
    def __init__(self, limit):
        '''
        Initialize the generator with an upper limit.
        Args:
            limit (int): The maximum Fibonacci value to generate (inclusive).
        Raises:
            ValueError: If the limit is negative.
        '''
        if limit < 0:
            raise ValueError("Limit must be a non-negative integer.")
        self.limit = limit
    def generate(self):
        '''
        Generate all Fibonacci numbers up to and including the limit.
        Returns:
            list[int]: A list of Fibonacci numbers where each number is <= limit.
        '''
        return generate_fibonacci_up_to(self.limit)
    def __iter__(self):
        '''
        Allow iteration over Fibonacci numbers up to the limit,
        yielding one number at a time without storing the whole list.
        '''
        a, b = 0, 1
        while a <= self.limit:
            yield a
            a, b = b, a + b
    def __str__(self):
        '''
        Return a human-readable, comma-separated string of the sequence.
        '''
        numbers = self.generate()
        return ", ".join(str(n) for n in numbers)
def generate_fibonacci_up_to(limit):
    '''
    Generate Fibonacci numbers up to a given limit (inclusive).
    The sequence starts at 0 and 1, and continues while the next
    number does not exceed the limit.
    Args:
        limit (int): The maximum Fibonacci value to generate (inclusive).
    Returns:
        list[int]: Fibonacci numbers not exceeding the limit.
    Raises:
        ValueError: If the limit is negative.
    '''
    if limit < 0:
        raise ValueError("Limit must be a non-negative integer.")
    numbers = []
    a, b = 0, 1
    while a <= limit:
        numbers.append(a)
        a, b = b, a + b
    return numbers