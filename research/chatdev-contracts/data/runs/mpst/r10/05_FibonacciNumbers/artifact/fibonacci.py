'''
Core Fibonacci number generation logic.
Provides the FibonacciGenerator class, which generates all Fibonacci
numbers up to a given (inclusive) upper limit. Two strategies are
implemented:
- generate(): an efficient iterative approach (default, O(n) time).
- generate_recursive(): a memoized bottom-up approach (educational
  alternative demonstrating memoization with zero recursion-depth
  risk, safe for arbitrarily large limits).
'''
class FibonacciGenerator:
    """Generates Fibonacci numbers up to a specified inclusive limit."""
    def __init__(self, limit):
        """Initialize the generator with an upper limit (inclusive).
        Args:
            limit (int): The maximum Fibonacci value to generate (>= 0).
        """
        self.limit = limit
    def generate(self):
        """Generate all Fibonacci numbers <= limit iteratively.
        Returns:
            list[int]: Fibonacci numbers from 0 up to and including limit.
        """
        numbers = []
        a, b = 0, 1
        while a <= self.limit:
            numbers.append(a)
            a, b = b, a + b
        return numbers
    def generate_recursive(self):
        """Generate all Fibonacci numbers <= limit using memoization
        (bottom-up computation, safe for arbitrarily large limits).
        Returns:
            list[int]: Fibonacci numbers from 0 up to and including limit.
        """
        memo = {0: 0, 1: 1}
        numbers = []
        index = 0
        while True:
            if index not in memo:
                memo[index] = memo[index - 1] + memo[index - 2]
            value = memo[index]
            if value > self.limit:
                break
            numbers.append(value)
            index += 1
        return numbers