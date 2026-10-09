'''
fibonacci.py
Core module of the Fibonacci Number Generator application. It defines the
FibonacciGenerator class, which produces every Fibonacci number up to a
user-specified limit using an efficient iterative algorithm, plus a
convenience function `fibonacci_up_to` for one-shot usage.
'''
class FibonacciGenerator:
    '''
    Generates all Fibonacci numbers up to (and including) a given limit.
    The sequence starts at 0 and 1, and each subsequent number is the sum
    of the two preceding ones. Generation stops as soon as the next
    Fibonacci number would exceed the configured limit. The iterative
    approach keeps the algorithm O(log(limit)) in memory-friendly steps
    and avoids the exponential cost of naive recursion.
    '''
    def __init__(self, limit):
        '''
        Initialize the generator with an upper limit and build the sequence.
        Args:
            limit (int): Maximum value a Fibonacci number may reach.
        Raises:
            ValueError: If limit is not an integer or is negative.
        '''
        if isinstance(limit, bool) or not isinstance(limit, int):
            raise ValueError("Limit must be an integer.")
        if limit < 0:
            raise ValueError("Limit must be a non-negative integer.")
        self._limit = limit
        self._sequence = self._build_sequence()
    def _build_sequence(self):
        '''
        Iteratively build the Fibonacci sequence up to the limit.
        Returns:
            list[int]: All Fibonacci numbers <= limit, in ascending order.
        '''
        sequence = []
        current, nxt = 0, 1
        while current <= self._limit:
            sequence.append(current)
            current, nxt = nxt, current + nxt
        return sequence
    def generate(self):
        '''
        Return a copy of the generated Fibonacci sequence.
        Returns:
            list[int]: The Fibonacci numbers up to the limit.
        '''
        return list(self._sequence)
    def as_list(self):
        '''
        Alias for generate(); returns the sequence as a plain list.
        Returns:
            list[int]: The Fibonacci numbers up to the limit.
        '''
        return self.generate()
    def count(self):
        '''
        Return how many Fibonacci numbers were generated.
        Returns:
            int: Number of terms in the sequence.
        '''
        return len(self._sequence)
    def total(self):
        '''
        Return the sum of all generated Fibonacci numbers.
        Returns:
            int: Sum of the sequence.
        '''
        return sum(self._sequence)
    def largest(self):
        '''
        Return the largest Fibonacci number not exceeding the limit.
        Returns:
            int or None: Largest generated number, or None if the
            sequence is empty (which cannot happen for limit >= 0,
            since 0 is always included).
        '''
        return self._sequence[-1] if self._sequence else None
    def __iter__(self):
        '''
        Allow iteration over the generated numbers (e.g. in for-loops).
        Returns:
            iterator: Iterator over the Fibonacci sequence.
        '''
        return iter(self._sequence)
    def __len__(self):
        '''
        Support len() on the generator object.
        Returns:
            int: Number of Fibonacci numbers generated.
        '''
        return len(self._sequence)
    def __repr__(self):
        '''
        Return a developer-friendly representation of the generator.
        Returns:
            str: Description including the limit and term count.
        '''
        return "FibonacciGenerator(limit={}, count={})".format(self._limit, self.count())
def fibonacci_up_to(limit):
    '''
    Convenience function: return all Fibonacci numbers up to a limit.
    Args:
        limit (int): Maximum Fibonacci value allowed.
    Returns:
        list[int]: Fibonacci numbers from 0 up to and including limit.
    Raises:
        ValueError: If limit is invalid (see FibonacciGenerator).
    '''
    return FibonacciGenerator(limit).generate()