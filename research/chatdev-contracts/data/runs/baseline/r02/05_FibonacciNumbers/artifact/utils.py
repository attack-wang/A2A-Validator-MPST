'''
utils.py
Utility helpers for the Fibonacci Generator application.
This module keeps supporting functionality out of the core logic:
input validation (`parse_non_negative_integer`) and result
presentation (`format_output`).
'''
def parse_non_negative_integer(raw_input):
    """
    Convert raw user input into a non-negative integer.
    Note: zero is a valid limit here (it yields the Fibonacci number 0),
    hence the name and error messages say "non-negative" rather than
    "positive".
    Args:
        raw_input (str): The raw string typed by the user.
    Returns:
        int: The parsed non-negative integer.
    Raises:
        ValueError: If the input is empty, not an integer, or negative.
    """
    text = str(raw_input).strip()
    if not text:
        raise ValueError("input cannot be empty")
    try:
        value = int(text)
    except ValueError:
        raise ValueError(f"'{text}' is not a valid integer")
    if value < 0:
        raise ValueError("the limit must be a non-negative integer")
    return value
def format_output(numbers, limit):
    """
    Build a human-readable, multi-line report of the generated numbers.
    Args:
        numbers (list[int]): Fibonacci numbers that were generated.
        limit (int): The upper limit that was used.
    Returns:
        str: Formatted report ready to be printed.
    """
    lines = [f"Fibonacci numbers up to {limit}:"]
    if not numbers:
        # Defensive branch: with the current validation a limit >= 0
        # always yields at least [0], so this is only reachable if
        # `format_output` is reused elsewhere with an empty list.
        lines.append("  (none found)")
    else:
        lines.append("  " + ", ".join(str(n) for n in numbers))
        lines.append(f"  Count: {len(numbers)}")
        lines.append(f"  Largest number generated: {numbers[-1]}")
    return "\n".join(lines)