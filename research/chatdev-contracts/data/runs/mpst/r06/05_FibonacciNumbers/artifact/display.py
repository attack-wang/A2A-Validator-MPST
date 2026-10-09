'''
display.py
Presentation module for the Fibonacci Generator application.
Formats and prints the generated Fibonacci sequence together with
a short statistical summary.
'''
LINE_WIDTH = 55
def display_fibonacci(numbers, limit):
    '''
    Display the generated Fibonacci numbers in a numbered list.
    Args:
        numbers (list[int]): The Fibonacci numbers to display.
        limit (int): The inclusive upper bound used for generation.
    '''
    print("\n" + "=" * LINE_WIDTH)
    print(f"Fibonacci numbers up to {limit} (inclusive):")
    print("=" * LINE_WIDTH)
    if not numbers:
        print("No Fibonacci numbers found within the given range.")
        print("=" * LINE_WIDTH)
        return
    for index, number in enumerate(numbers, start=1):
        print(f"  {index:>3}. {number}")
    print("=" * LINE_WIDTH)
def display_summary(numbers):
    '''
    Display a short summary of the generated sequence.
    Args:
        numbers (list[int]): The generated Fibonacci numbers.
    '''
    if not numbers:
        return
    print("-" * LINE_WIDTH)
    print(f"  Count of numbers generated : {len(numbers)}")
    print(f"  Largest Fibonacci number   : {numbers[-1]}")
    print(f"  Sum of all numbers         : {sum(numbers)}")
    print("=" * LINE_WIDTH)