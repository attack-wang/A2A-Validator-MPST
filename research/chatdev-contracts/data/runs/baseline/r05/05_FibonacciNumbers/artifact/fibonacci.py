'''
Fibonacci Module
Core logic for generating Fibonacci numbers up to a given limit.
Provides two implementations:
  - generate_fibonacci(limit): returns the full sequence as a list.
  - fibonacci_generator(limit): a memory-efficient generator that
    yields numbers one at a time (useful for very large limits).
The sequence produced starts at 0 and 1, and every subsequent
number is the sum of the previous two:
    0, 1, 1, 2, 3, 5, 8, 13, 21, ...
'''
def generate_fibonacci(limit):
    '''
    Generate a list of Fibonacci numbers up to and including the limit.
    Args:
        limit (int): The maximum value (inclusive) for generated numbers.
    Returns:
        list: Fibonacci numbers, each of which is less than or equal to limit.
    Raises:
        ValueError: If limit is negative.
    '''
    if limit < 0:
        raise ValueError("Limit must be a non-negative integer.")
    numbers = []
    a, b = 0, 1
    while a <= limit:
        numbers.append(a)
        a, b = b, a + b
    return numbers
def fibonacci_generator(limit):
    '''
    Yield Fibonacci numbers up to and including the limit, one at a time.
    Memory-efficient alternative to generate_fibonacci(): numbers are
    produced lazily instead of being stored in a list.
    Args:
        limit (int): The maximum value (inclusive) for generated numbers.
    Yields:
        int: The next Fibonacci number that is less than or equal to limit.
    Raises:
        ValueError: If limit is negative.
    '''
    if limit < 0:
        raise ValueError("Limit must be a non-negative integer.")
    a, b = 0, 1
    while a <= limit:
        yield a
        a, b = b, a + b