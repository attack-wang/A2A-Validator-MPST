'''
cli.py
Command-line interface for the Palindrome Detector application.
Functions:
    build_parser -- creates the argparse parser for the CLI options.
    run_cli      -- parses arguments, analyses the file and prints/saves
                    the resulting report.
'''
import argparse
import sys
from file_handler import FileHandler
from palindrome_detector import PalindromeDetector
def build_parser():
    """Create and return the argument parser for the command line."""
    parser = argparse.ArgumentParser(
        prog='palindrome_detector',
        description='Detect palindromic words and phrases in a text file.',
    )
    parser.add_argument('file', help='Path to the text file to analyse.')
    parser.add_argument(
        '-o', '--output',
        help='Optional path of a report file to write the results to.',
    )
    parser.add_argument(
        '--min-length', type=int, default=2, metavar='N',
        help='Minimum normalized length for a palindrome candidate (default: 2).',
    )
    parser.add_argument(
        '--case-sensitive', action='store_true',
        help='Treat uppercase and lowercase letters as different.',
    )
    return parser
def run_cli(argv=None):
    """
    Execute the command-line workflow.
    Args:
        argv (list[str] | None): Raw command-line arguments (without the
            program name). Defaults to sys.argv[1:] when None.
    Returns:
        int: Process exit code (0 on success, 1 on failure).
    """
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        text = FileHandler.read_file(args.file)
    except (FileNotFoundError, UnicodeDecodeError, OSError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    detector = PalindromeDetector(
        min_length=args.min_length,
        case_sensitive=args.case_sensitive,
    )
    result = detector.analyze(text)
    report = FileHandler.format_report(args.file, result)
    print(report)
    if args.output:
        try:
            FileHandler.write_report(args.output, report)
            print(f"Report saved to: {args.output}")
        except OSError as error:
            print(f"Error: could not write report - {error}", file=sys.stderr)
            return 1
    return 0