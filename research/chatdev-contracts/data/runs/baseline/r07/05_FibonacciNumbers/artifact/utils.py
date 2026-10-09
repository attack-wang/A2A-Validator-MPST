'''
utils.py
Utility helpers for the Fibonacci Generator application.
This module provides:
- format_sequence: formats a list of numbers into a readable, wrapped string.
- build_argument_parser: creates the command-line argument parser.
'''
import argparse
def format_sequence(numbers, per_line=10):
    """
    Format a sequence of numbers into a human-readable string.
    Numbers are separated by commas and wrapped onto new lines after
    `per_line` numbers to keep the output tidy for long sequences.
    Args:
        numbers (list): The numbers to format.
        per_line (int): Maximum numbers displayed per line (default 10).
    Returns:
        str: The formatted sequence string, or a placeholder message
             if the sequence is empty.
    """
    if not numbers:
        return "(no Fibonacci numbers to display)"
    lines = []
    for start in range(0, len(numbers), per_line):
        chunk = numbers[start:start + per_line]
        lines.append(", ".join(str(n) for n in chunk))
    return "\n".join(lines)
def build_argument_parser():
    """
    Build the command-line argument parser for the application.
    Returns:
        argparse.ArgumentParser: Configured parser accepting an optional
        positional `limit` argument. If the limit is omitted, the
        application runs in interactive mode.
    """
    parser = argparse.ArgumentParser(
        description="Generate Fibonacci numbers up to a given number."
    )
    parser.add_argument(
        "limit",
        nargs="?",
        default=None,
        help="Upper bound (inclusive) for generated Fibonacci numbers. "
             "If omitted, the program runs in interactive mode."
    )
    return parser