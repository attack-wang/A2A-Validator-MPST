'''
cli.py
Command-line interface layer for the Fibonacci Number Generator.
Responsibilities:
- Define and parse command-line arguments (build_parser).
- Format Fibonacci sequences for console display (format_sequence).
- Execute the one-shot command-line workflow (run_cli).
'''
import argparse
from typing import Iterable, List
from fibonacci import generate_fibonacci_up_to, parse_limit
def build_parser() -> argparse.ArgumentParser:
    """
    Construct the argument parser for the application.
    Returns
    -------
    argparse.ArgumentParser
        Parser accepting an optional positional ``limit`` (non-negative
        integer) and an ``-i/--interactive`` flag.
    """
    parser = argparse.ArgumentParser(
        prog="fibonacci_app",
        description=(
            "Generate all Fibonacci numbers up to (and including) a given "
            "non-negative integer limit."
        ),
        epilog=(
            "Examples:\n"
            "  python main.py 100   -> prints Fibonacci numbers <= 100\n"
            "  python main.py -i    -> starts interactive mode"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "limit",
        nargs="?",
        default=None,
        metavar="LIMIT",
        help="inclusive upper bound for Fibonacci numbers (non-negative integer)",
    )
    parser.add_argument(
        "-i",
        "--interactive",
        action="store_true",
        help="run in interactive mode and prompt for limits until you quit",
    )
    return parser
def format_sequence(numbers: Iterable[int]) -> str:
    """
    Format a sequence of Fibonacci numbers for console display.
    Parameters
    ----------
    numbers : Iterable[int]
        The Fibonacci numbers to format.
    Returns
    -------
    str
        A comma-separated representation, or a friendly message when the
        sequence is empty.
    """
    values: List[int] = list(numbers)
    if not values:
        return "No Fibonacci numbers to display for the given limit."
    return ", ".join(str(value) for value in values)
def run_cli(args: argparse.Namespace) -> int:
    """
    Execute the application in one-shot command-line mode.
    Parameters
    ----------
    args : argparse.Namespace
        Parsed command-line arguments containing ``limit``.
    Returns
    -------
    int
        Exit code: 0 on success, 1 when the limit is missing or invalid.
    """
    if args.limit is None:
        # Defensive guard: a LIMIT is required in one-shot mode.
        print("Error: a LIMIT is required unless -i/--interactive is used.")
        print("Run 'python main.py --help' for usage information.")
        return 1
    try:
        limit = parse_limit(args.limit)  # args.limit is already a string
    except ValueError as exc:
        print(f"Error: {exc}")
        print("Run 'python main.py --help' for usage information.")
        return 1
    numbers = generate_fibonacci_up_to(limit)
    print(f"Fibonacci numbers up to {limit}:")
    print(format_sequence(numbers))
    print(f"Count: {len(numbers)}")
    return 0