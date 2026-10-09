'''
utils.py
Utility helpers for the Fibonacci Number Generator application. This module
is responsible for validating and parsing user input, formatting the
generated sequence into readable columns, and printing the console banner
and summary statistics.
'''
def parse_limit(raw_value):
    '''
    Convert raw user input into a validated non-negative integer.
    Args:
        raw_value (str or int): The raw input from the console or CLI.
    Returns:
        int: The parsed, validated limit.
    Raises:
        ValueError: If the input is empty, not an integer, or negative.
    '''
    if raw_value is None:
        raise ValueError("No limit provided.")
    text = str(raw_value).strip()
    if not text:
        raise ValueError("Input is empty. Please enter a non-negative integer.")
    try:
        value = int(text)
    except ValueError:
        raise ValueError("'{}' is not a valid integer.".format(text)) from None
    if value < 0:
        raise ValueError("The limit must be zero or a positive integer.")
    return value
def format_sequence(numbers, per_line=10, field_width=None):
    '''
    Format a list of numbers into readable, column-aligned text.
    Args:
        numbers (list[int]): Numbers to format.
        per_line (int): Maximum numbers displayed per line (must be >= 1).
        field_width (int or None): Column width; auto-sized from the
            largest number when None.
    Returns:
        str: The formatted, multi-line string.
    Raises:
        ValueError: If per_line is less than 1.
    '''
    if not numbers:
        return "(no Fibonacci numbers to display)"
    if per_line < 1:
        raise ValueError("per_line must be a positive integer.")
    if field_width is None:
        field_width = len(str(numbers[-1])) + 2
    field_width = max(1, field_width)
    lines = []
    for start in range(0, len(numbers), per_line):
        chunk = numbers[start:start + per_line]
        lines.append(" ".join(str(n).rjust(field_width) for n in chunk))
    return "\n".join(lines)
def print_banner():
    '''
    Print the application banner to the console.
    '''
    print("=" * 52)
    print("        Fibonacci Number Generator (Python)")
    print("=" * 52)
def print_summary(numbers):
    '''
    Print summary statistics about the generated sequence.
    Args:
        numbers (list[int]): The generated Fibonacci numbers.
    '''
    print("-" * 52)
    if not numbers:
        print("Summary: no Fibonacci numbers fall within this limit.")
        return
    print("Terms generated : {}".format(len(numbers)))
    print("Largest term    : {}".format(numbers[-1]))
    print("Sum of all terms: {}".format(sum(numbers)))