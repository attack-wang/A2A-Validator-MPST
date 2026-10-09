'''
fibonacci.py
Core Fibonacci generation logic.
Provides a memory-efficient generator that lazily yields Fibonacci
numbers up to a limit, plus an eager helper returning them as a list.
'''
def fibonacci_generator(limit):
    '''
    Lazily yield every Fibonacci number that does not exceed the limit.
    Args:
        limit (int): Maximum value (inclusive) a Fibonacci number may reach.
    Yields:
        int: The next Fibonacci number not exceeding the limit.
    '''
    a, b = 0, 1
    while a <= limit:
        yield a
        a, b = b, a + b
def generate_fibonacci_up_to(limit):
    '''
    Return all Fibonacci numbers up to (and including) the limit.
    Args:
        limit (int): Maximum value (inclusive) a Fibonacci number may reach.
    Returns:
        list[int]: Fibonacci numbers in ascending order, all <= limit.
    Raises:
        TypeError: If limit is not an integer.
        ValueError: If limit is negative.
    '''
    if isinstance(limit, bool) or not isinstance(limit, int):
        raise TypeError("limit must be an integer")
    if limit < 0:
        raise ValueError("limit must be non-negative")
    return list(fibonacci_generator(limit))