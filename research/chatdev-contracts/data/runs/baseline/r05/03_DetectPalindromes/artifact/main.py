'''
main.py
Entry point for the Palindrome Detector application. Parses command-line
arguments, reads the target text file, runs the palindrome analysis, and
prints (and optionally saves) a report of the findings.
'''
import argparse
import sys
from file_handler import FileHandler
from palindrome_detector import PalindromeDetector
from report_generator import ReportGenerator
def parse_arguments(argv=None):
    '''
    Parse command-line arguments.
    The positional filepath is optional so that the standalone
    --check mode can be used without providing a text file.
    Args:
        argv (list): Optional argument list (defaults to sys.argv).
    Returns:
        argparse.Namespace: Parsed arguments.
    '''
    parser = argparse.ArgumentParser(
        description="Detect palindromes in a given text file."
    )
    parser.add_argument(
        "filepath",
        nargs="?",
        default=None,
        help="Path to the text file to analyze (required unless --check is used)."
    )
    parser.add_argument(
        "-o", "--output",
        help="Optional path to save the report as a text file.",
        default=None
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Strict mode: consider case and punctuation when checking."
    )
    parser.add_argument(
        "--check",
        help="Check a single word or phrase for palindromicity and exit.",
        default=None
    )
    return parser.parse_args(argv)
def main():
    '''
    Run the palindrome detection workflow.
    '''
    args = parse_arguments()
    detector = PalindromeDetector(
        ignore_case=not args.strict,
        ignore_non_alphanumeric=not args.strict
    )
    # Single phrase check mode (no filepath required)
    if args.check:
        result = detector.is_palindrome(args.check)
        status = "IS" if result else "is NOT"
        print(f'The phrase "{args.check}" {status} a palindrome.')
        sys.exit(0)
    # File analysis mode: a filepath must be supplied
    if not args.filepath:
        print("Error: a text file path is required "
              "(or use --check to test a single word or phrase).")
        sys.exit(1)
    # File analysis mode
    try:
        text = FileHandler.read_text_file(args.filepath)
    except FileNotFoundError as error:
        print(f"Error: {error}")
        sys.exit(1)
    except OSError as error:
        print(f"Error reading file: {error}")
        sys.exit(1)
    if not text.strip():
        print("The provided file is empty. Nothing to analyze.")
        sys.exit(1)
    analysis = detector.analyze(text)
    report = ReportGenerator.generate_report(analysis, source_name=args.filepath)
    print(report)
    if args.output:
        try:
            ReportGenerator.save_report(report, args.output)
            print(f"Report saved to: {args.output}")
        except OSError as error:
            print(f"Error saving report: {error}")
            sys.exit(1)
if __name__ == "__main__":
    main()