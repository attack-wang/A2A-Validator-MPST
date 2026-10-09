'''
input_handler.py
User interaction module for the Fibonacci Generator application.
Responsible for reading raw user input, validating it as a
non-negative integer, and asking simple yes/no questions.
This version handles closed or interrupted input streams
(EOFError / KeyboardInterrupt) by raising a dedicated
InputClosedError, so the application can exit cleanly instead
of crashing with a raw traceback (e.g., in automated test runs
or piped/redirected empty input).
'''
class InputClosedError(Exception):
    '''Raised when the input stream is closed (EOF) or interrupted.'''
def validate_input(raw_value):
    '''
    Validate that a raw string represents a non-negative integer.
    Args:
        raw_value (str): The raw string entered by the user.
    Returns:
        int: The parsed non-negative integer.
    Raises:
        ValueError: If the input is empty, not an integer, or negative.
    '''
    raw_value = raw_value.strip()
    if not raw_value:
        raise ValueError("input cannot be empty")
    try:
        value = int(raw_value)
    except ValueError:
        raise ValueError(f"'{raw_value}' is not a valid integer")
    if value < 0:
        raise ValueError("the number must be non-negative")
    return value
def get_user_input(prompt="Enter a number: "):
    '''
    Prompt the user repeatedly until a valid non-negative integer
    is provided.
    Args:
        prompt (str): The message displayed to the user.
    Returns:
        int: A validated non-negative integer.
    Raises:
        InputClosedError: If the input stream is closed (EOF) or
            interrupted by the user.
    '''
    while True:
        try:
            line = input(prompt)
        except EOFError:
            raise InputClosedError("Input stream closed (EOF).")
        except KeyboardInterrupt:
            raise InputClosedError("Interrupted by user.")
        try:
            return validate_input(line)
        except ValueError as error:
            print(f"Invalid input: {error}. Please try again.")
def ask_yes_no(prompt):
    '''
    Ask a yes/no question and interpret the answer.
    Args:
        prompt (str): The yes/no question displayed to the user.
    Returns:
        bool: True if the user answers 'y'/'yes', False if 'n'/'no'.
    Raises:
        InputClosedError: If the input stream is closed (EOF) or
            interrupted by the user.
    '''
    while True:
        try:
            answer = input(prompt).strip().lower()
        except (EOFError, KeyboardInterrupt):
            raise InputClosedError("Input stream closed (EOF).")
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Please answer with 'y' (yes) or 'n' (no).")