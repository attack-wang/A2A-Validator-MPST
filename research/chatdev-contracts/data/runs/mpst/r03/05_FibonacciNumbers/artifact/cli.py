'''
cli.py
Command-line interface layer for the Fibonacci Generator.
Responsible for argument parsing, input validation, the interactive
prompt loop, and printing generated sequences to the console.
'''
import argparse
import sys
from fibonacci import generate_fibonacci_up_to
def build_parser():
    '''
    Construct and configure the argparse parser.
    Returns:
        argparse.ArgumentParser: Parser accepting an optional -n/--number flag.
    '''
    parser = argparse.ArgumentParser(
        prog="fibonacci_app",
        description="Generate Fibonacci numbers up to a given number."
    )
    parser.add_argument(
        "-n", "--number",
        type=int,
        default=None,
        help="Upper limit (inclusive). Omit to enter interactive mode."
    )
    return parser
def parse_arguments(argv=None):
    '''
    Parse command-line arguments.
    Args:
        argv (list[str] | None): Raw argument list; defaults to sys.argv[1:].
    Returns:
        argparse.Namespace: Parsed arguments exposing a 'number' attribute.
    '''
    return build_parser().parse_args(argv)
def print_fibonacci(limit):
    '''
    Generate Fibonacci numbers up to the limit and print them.
    Args:
        limit (int): Upper bound (inclusive) for generated numbers.
    '''
    numbers = generate_fibonacci_up_to(limit)
    print(f"Fibonacci numbers up to {limit}:")
    if numbers:
        print(", ".join(str(n) for n in numbers))
    else:
        print("(none)")
    print(f"Total count: {len(numbers)}")
def read_positive_integer(prompt):
    '''
    Prompt until the user supplies a valid non-negative integer or quits.
    Args:
        prompt (str): Text shown to the user.
    Returns:
        int | None: Parsed integer, or None if the user chose to quit.
    '''
    while True:
        raw = input(prompt).strip().lower()
        if raw in ("q", "quit", "exit"):
            return None
        try:
            value = int(raw)
        except ValueError:
            print("Invalid input: please enter a non-negative integer.\n")
            continue
        if value < 0:
            print("Invalid input: the number must be non-negative.\n")
            continue
        return value
def run_interactive():
    '''
    Run the interactive loop: repeatedly ask for limits and print
    Fibonacci sequences until the user quits.
    '''
    print("=== Fibonacci Generator (interactive mode) ===")
    print("Enter a non-negative integer to list Fibonacci numbers up to it.")
    print("Type 'q' to quit.\n")
    while True:
        limit = read_positive_integer("Enter a number (or 'q' to quit): ")
        if limit is None:
            print("Goodbye!")
            break
        print_fibonacci(limit)
        print()
def run(args):
    '''
    Dispatch execution based on parsed arguments.
    Args:
        args (argparse.Namespace): Parsed CLI arguments.
    '''
    if args.number is None:
        run_interactive()
    elif args.number < 0:
        print("Error: the number must be non-negative.", file=sys.stderr)
        sys.exit(1)
    else:
        print_fibonacci(args.number)