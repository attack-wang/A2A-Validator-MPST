'''
utils.py
Utility module of the Fibonacci Generator application.
Provides input parsing and validation helpers used by main.py to safely
obtain a non-negative integer upper limit from the user.
'''
def parse_limit(raw_input):
    """Convert raw user input into a validated non-negative integer.
    Args:
        raw_input (str): The raw text typed by the user.
    Returns:
        int: The validated non-negative integer limit.
    Raises:
        ValueError: If the input is empty, not an integer, or negative.
    """
    text = raw_input.strip()
    if not text:
        raise ValueError("input is empty")
    try:
        value = int(text)
    except ValueError:
        # 'from None' suppresses the noisy exception-chaining traceback.
        raise ValueError(f"'{text}' is not a valid integer") from None
    if value < 0:
        raise ValueError("the limit must be a non-negative integer")
    return value
def get_valid_limit(prompt="Enter the upper limit for Fibonacci numbers: "):
    """Prompt the user repeatedly until a valid non-negative integer is given.
    Args:
        prompt (str): The message displayed to the user.
    Returns:
        int: A validated non-negative integer limit.
    """
    while True:
        raw = input(prompt)
        try:
            return parse_limit(raw)
        except ValueError as error:
            print(f"Invalid input: {error}. Please try again.")