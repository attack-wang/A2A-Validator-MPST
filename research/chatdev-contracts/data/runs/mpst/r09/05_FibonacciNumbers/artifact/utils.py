'''
utils.py
Helper utilities for input validation, parsing, and output formatting
used by the Fibonacci Generator application.
'''
def parse_limit(raw_value):
    """
    Parse and validate a user-supplied value as a non-negative integer.
    Args:
        raw_value (str): The raw input string.
    Returns:
        int: The parsed non-negative integer.
    Raises:
        ValueError: If the input is empty, not an integer, or negative.
    """
    text = str(raw_value).strip()
    if not text:
        raise ValueError("Input cannot be empty. "
                         "Please enter a non-negative integer.")
    try:
        value = int(text)
    except ValueError:
        raise ValueError(f"'{text}' is not a valid integer.")
    if value < 0:
        raise ValueError("Please enter a non-negative integer (0 or greater).")
    return value
def format_sequence(numbers, per_line=10):
    """
    Format a sequence of numbers as a human-readable multi-line string.
    Args:
        numbers (list[int]): The numbers to format.
        per_line (int): Maximum numbers displayed per line.
    Returns:
        str: Comma-separated numbers wrapped every `per_line` items,
             or a friendly message if the sequence is empty.
    """
    if not numbers:
        return "No Fibonacci numbers found for the given input."
    lines = []
    for start in range(0, len(numbers), per_line):
        chunk = numbers[start:start + per_line]
        lines.append(", ".join(str(n) for n in chunk))
    return "\n".join(lines)
def build_summary(numbers, label):
    """
    Build a short one-line summary describing the generated sequence.
    Args:
        numbers (list[int]): Generated Fibonacci numbers.
        label (str): Human-readable description of the generation criterion.
    Returns:
        str: A one-line summary, e.g.
             "Found 8 Fibonacci number(s) for limit 20 (largest: 13)."
    """
    count = len(numbers)
    if not numbers:
        return f"No Fibonacci numbers found for {label}."
    largest = numbers[-1]
    return (f"Found {count} Fibonacci number(s) for {label} "
            f"(largest: {largest}).")