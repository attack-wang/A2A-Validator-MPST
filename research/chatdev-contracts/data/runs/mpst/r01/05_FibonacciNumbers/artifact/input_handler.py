'''
input_handler.py
This module handles user input for the Fibonacci application. It provides
functions to prompt the user for a number and validate that the input is
a non-negative integer, ensuring the application never crashes on bad input.
'''
def get_user_input():
    """
    Prompt the user for a number and return it as a validated integer.
    Repeatedly prompts the user until a valid non-negative integer
    is provided.
    Returns:
        int: A non-negative integer entered by the user.
    """
    while True:
        raw_value = input("Enter a number to generate Fibonacci numbers up to it: ").strip()
        try:
            value = validate_positive_integer(raw_value)
            return value
        except ValueError as error:
            print(f"Invalid input: {error}. Please try again.")
def validate_positive_integer(value):
    """
    Validate that the given string represents a non-negative integer.
    Args:
        value (str): The raw string input to validate.
    Returns:
        int: The validated non-negative integer.
    Raises:
        ValueError: If the input is not a valid non-negative integer.
    """
    try:
        number = int(value)
    except (TypeError, ValueError):
        raise ValueError("the value must be an integer")
    if number < 0:
        raise ValueError("the value must be non-negative")
    return number