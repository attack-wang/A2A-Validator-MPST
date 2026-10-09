'''
Module: utils.py
This module provides helper utilities for the Fibonacci application,
including user-input validation and human-friendly output formatting.
'''
def validate_input(user_input):
    """
    Validate raw user input and convert it to a non-negative integer.
    Args:
        user_input (str): The raw input string from the user.
    Returns:
        int: The validated non-negative integer.
    Raises:
        ValueError: If the input is not a valid integer or is negative.
    """
    try:
        value = int(str(user_input).strip())
    except (ValueError, TypeError):
        raise ValueError(f"'{user_input}' is not a valid integer.")
    if value < 0:
        raise ValueError("The number must be non-negative (>= 0).")
    return value
def format_output(numbers, limit):
    """
    Format the generated Fibonacci numbers into a readable report.
    Args:
        numbers (list[int]): The generated Fibonacci numbers.
        limit (int): The limit that was used for generation.
    Returns:
        str: A formatted, multi-line string ready to be printed.
    """
    if not numbers:
        return f"No Fibonacci numbers found up to {limit}."
    lines = [
        f"Fibonacci numbers up to {limit} ({len(numbers)} number(s) found):"
    ]
    for index, number in enumerate(numbers, start=1):
        lines.append(f"  {index:>3}. {number}")
    return "\n".join(lines)