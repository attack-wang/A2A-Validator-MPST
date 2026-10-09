'''
Utility Module
Helper functions used by the Fibonacci Number Generator application:
  - validate_input(): parses and validates raw user input.
  - format_output(): builds a readable, formatted result string.
'''
def validate_input(input_str):
    '''
    Validate a raw input string and convert it to a non-negative integer.
    Args:
        input_str (str): The raw string entered by the user.
    Returns:
        int: The parsed non-negative integer.
    Raises:
        ValueError: If the input is empty, not an integer, or negative.
    '''
    input_str = input_str.strip()
    if not input_str:
        raise ValueError("Input cannot be empty.")
    try:
        value = int(input_str)
    except ValueError:
        raise ValueError(f"'{input_str}' is not a valid integer.") from None
    if value < 0:
        raise ValueError("Please enter a non-negative integer.")
    return value
def format_output(numbers, limit):
    '''
    Format the generated Fibonacci numbers into a readable output string.
    Args:
        numbers (list): The Fibonacci numbers to display.
        limit (int): The limit used to generate the numbers.
    Returns:
        str: A formatted, human-readable output string.
    '''
    header = f"Fibonacci numbers up to {limit}:"
    if numbers:
        body = ", ".join(str(number) for number in numbers)
    else:
        body = "(no Fibonacci numbers found)"
    summary = f"Total count: {len(numbers)}"
    return f"{header}\n  {body}\n{summary}"