'''
utils.py
Utility helpers for presenting results to the user.
'''
def print_result(numbers: list, limit: int) -> None:
    """
    Print the generated Fibonacci sequence in a user-friendly format.
    Args:
        numbers: List of Fibonacci numbers up to the limit.
        limit: The upper bound used for generation.
    """
    print(f"\nFibonacci numbers up to {limit}:")
    if not numbers:
        print("  (no Fibonacci numbers found)")
        return
    print(", ".join(str(n) for n in numbers))
    print(f"Total: {len(numbers)} number(s)")