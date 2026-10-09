'''
cli.py
Command-line interface layer for the Fibonacci application:
argument parsing, interactive prompting, and output formatting.
'''
import argparse
from fibonacci import fibonacci_generator, generate_fibonacci
from utils import InputValidationError, parse_integer, validate_limit
def build_argument_parser():
    '''
    Construct the argparse parser for the application.
    Returns:
        argparse.ArgumentParser: Parser with an optional positional `limit`,
        a `--count` flag, and a `--stream` flag.
    '''
    parser = argparse.ArgumentParser(
        prog="fibonacci_app",
        description="Generate Fibonacci numbers up to a given number.",
    )
    parser.add_argument(
        "limit",
        nargs="?",
        type=int,
        default=None,
        help="Inclusive upper bound for the Fibonacci numbers; "
             "if omitted, the program asks for it interactively.",
    )
    parser.add_argument(
        "-c", "--count",
        action="store_true",
        help="Also print how many Fibonacci numbers were generated.",
    )
    parser.add_argument(
        "-s", "--stream",
        action="store_true",
        help="Print numbers one per line as they are generated "
             "(memory-efficient streaming mode).",
    )
    return parser
def prompt_for_limit():
    '''
    Interactively ask the user for a limit, re-prompting on invalid input.
    Returns:
        int: A validated non-negative integer limit.
    Raises:
        EOFError: If the input stream is closed (propagates to main).
        KeyboardInterrupt: If the user presses Ctrl+C (propagates to main).
    '''
    while True:
        try:
            raw = input("Enter the upper limit for Fibonacci numbers: ")
            return validate_limit(parse_integer(raw))
        except InputValidationError as error:
            print(f"Invalid input: {error}")
def format_output(numbers, limit, show_count=False):
    '''
    Build a human-readable report of generated Fibonacci numbers.
    Args:
        numbers (list[int]): Fibonacci numbers <= limit, ascending.
        limit (int): The requested upper bound.
        show_count (bool): Whether to append the count of numbers.
    Returns:
        str: Multi-line report ready to be printed.
    '''
    lines = [f"Fibonacci numbers up to {limit}:"]
    if numbers:
        lines.append("  " + ", ".join(str(number) for number in numbers))
    else:
        lines.append("  (none)")
    if show_count:
        lines.append(f"Count: {len(numbers)}")
    return "\n".join(lines)
def stream_numbers(limit):
    '''
    Print Fibonacci numbers up to `limit` one per line, as they are
    produced by the lazy generator.
    Args:
        limit (int): Inclusive upper bound.
    '''
    print(f"Fibonacci numbers up to {limit}:")
    for number in fibonacci_generator(limit):
        print(f"  {number}")
def main(argv=None):
    '''
    Entry point: parse arguments, obtain a validated limit, and print
    the Fibonacci numbers up to that limit.
    Args:
        argv (list[str] | None): Command-line arguments; None means sys.argv.
    Returns:
        int: Process exit code (0 on success, 1 on invalid input).
    '''
    parser = build_argument_parser()
    args = parser.parse_args(argv)
    try:
        limit = prompt_for_limit() if args.limit is None else validate_limit(args.limit)
    except InputValidationError as error:
        print(f"Error: {error}")
        return 1
    if args.stream:
        stream_numbers(limit)
    else:
        print(format_output(generate_fibonacci(limit), limit, show_count=args.count))
    return 0