def fibonacci_up_to(limit):
    """Return a list of Fibonacci numbers less than or equal to limit."""
    numbers = []
    a, b = 0, 1
    while a <= limit:
        numbers.append(a)
        a, b = b, a + b
    return numbers