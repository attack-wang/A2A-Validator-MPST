'''
utils.py
Utility helpers for parsing user input and formatting program output.
Keeps validation and presentation concerns separate from the core
Fibonacci generation logic.
'''
def parse_input(raw_input):
    '''
    Parse a raw string into a non-negative integer.
    Args:
        raw_input (str): The raw text entered by the user.
    Returns:
        int: The parsed non-negative integer.
    Raises:
        ValueError: If the input is empty, not an integer, or negative.
    '''
    text = raw_input.strip()
    if not text:
        raise ValueError("Input cannot be empty.")
    try:
        value = int(text)
    except ValueError:
        raise ValueError(f"'{text}' is not a valid integer.")
    if value < 0:
        raise ValueError("Please enter a non-negative integer.")
    return value
def format_output(numbers):
    '''
    Format a list of Fibonacci numbers for display.
    Args:
        numbers (list[int]): The Fibonacci numbers to format.
    Returns:
        str: A formatted, human-readable string.
    '''
    if not numbers:
        return "No Fibonacci numbers found within the given limit."
    return ("Fibonacci numbers up to the limit:\n"
            + ", ".join(str(n) for n in numbers))