'''
utils.py
Utility helpers for parsing user input and formatting output.
Provides:
    * parse_non_negative_integer(text) -> parse a string into a non-negative int
    * format_sequence(numbers)         -> format an iterable of ints as a string
'''
def parse_non_negative_integer(text):
    '''
    Parse a string into a non-negative integer.
    Args:
        text (str): The raw user input to parse.
    Returns:
        int: The parsed non-negative integer.
    Raises:
        ValueError: If text is not a string, is empty, contains non-digit
            characters (including signs or decimal points), or cannot be
            interpreted as a non-negative integer.
    Examples:
        >>> parse_non_negative_integer("100")
        100
        >>> parse_non_negative_integer("  42  ")
        42
    '''
    if not isinstance(text, str):
        raise ValueError(f"'{text}' is not a valid non-negative integer.")
    stripped = text.strip()
    # isascii() + isdigit() rejects: empty strings, "-5", "3.14", "1e3",
    # and Unicode digits like '²' that isdigit() accepts but int() rejects.
    if not (stripped.isascii() and stripped.isdigit()):
        raise ValueError(f"'{text}' is not a valid non-negative integer.")
    return int(stripped)
def format_sequence(numbers):
    '''
    Format an iterable of integers (list or generator) as a readable,
    comma-separated string.
    Args:
        numbers (iterable[int]): The numbers to format.
    Returns:
        str: Comma-separated representation, e.g. "0, 1, 1, 2, 3".
    Examples:
        >>> format_sequence([0, 1, 1, 2, 3])
        '0, 1, 1, 2, 3'
    '''
    return ", ".join(str(number) for number in numbers)