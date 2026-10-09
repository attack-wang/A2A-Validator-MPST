'''
Main entry point for the Palindrome Detector application.
This module orchestrates the complete workflow:
1. Parse command-line arguments (input file, options, optional output report).
2. Read the given text file.
3. Detect palindromic words (and optionally palindromic lines).
4. Generate a human-readable report, print it to the console,
   and optionally save it to a file.
Usage example:
    python main.py sample_text.txt
    python main.py sample_text.txt --check-lines --min-length 3 -o report.txt
'''
import argparse
import sys
from palindrome_detector import PalindromeDetector
from file_handler import read_text_file, write_text_file
from report_generator import ReportGenerator
def positive_int(value):
    """
    Argparse type validator: accept only integers greater than zero.
    :param value: The raw string value supplied on the command line.
    :return: The validated positive integer.
    :raises argparse.ArgumentTypeError: If the value is not a positive integer.
    """
    try:
        number = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{value}' is not an integer.")
    if number < 1:
        raise argparse.ArgumentTypeError(
            "minimum length must be a positive integer (>= 1)."
        )
    return number
def parse_arguments():
    """Define and parse the command-line interface, returning the arguments."""
    parser = argparse.ArgumentParser(
        description="Detect palindromes in a given text file."
    )
    parser.add_argument(
        "input_file",
        help="Path to the text file to analyze."
    )
    parser.add_argument(
        "-o", "--output",
        default=None,
        help="Optional path to save the generated report as a text file."
    )
    parser.add_argument(
        "--case-sensitive",
        action="store_true",
        help="Treat uppercase and lowercase letters as different characters."
    )
    parser.add_argument(
        "--keep-punctuation",
        action="store_true",
        help="Do not strip punctuation and spaces when checking palindromes "
             "(mainly affects whole-line detection)."
    )
    parser.add_argument(
        "--min-length",
        type=positive_int,
        default=1,
        help="Minimum number of characters a word must have to be considered "
             "(default: 1). Use e.g. 3 to skip trivial single-letter palindromes."
    )
    parser.add_argument(
        "--check-lines",
        action="store_true",
        help="Additionally check whether entire lines are palindromes."
    )
    return parser.parse_args()
def main():
    """Run the palindrome detection workflow end to end."""
    args = parse_arguments()
    # Step 1: read the input file.
    try:
        text = read_text_file(args.input_file)
    except FileNotFoundError:
        print(f"Error: file '{args.input_file}' was not found.", file=sys.stderr)
        sys.exit(1)
    except UnicodeDecodeError as error:
        print(f"Error: could not decode '{args.input_file}' as text: {error}",
              file=sys.stderr)
        sys.exit(1)
    except OSError as error:
        print(f"Error: could not read '{args.input_file}': {error}", file=sys.stderr)
        sys.exit(1)
    # Step 2: configure the detector with the user's options.
    detector = PalindromeDetector(
        case_sensitive=args.case_sensitive,
        ignore_punctuation=not args.keep_punctuation,
        min_length=args.min_length,
    )
    # Step 3: run detection.
    word_palindromes = detector.find_palindrome_words(text)
    line_palindromes = detector.find_palindrome_lines(text) if args.check_lines else None
    # Step 4: build and display the report.
    generator = ReportGenerator(source_file=args.input_file)
    report = generator.generate(word_palindromes, line_palindromes)
    print(report)
    # Step 5: optionally persist the report to disk.
    if args.output:
        try:
            write_text_file(args.output, report)
            print(f"Report saved to '{args.output}'.")
        except OSError as error:
            print(f"Error: could not write report to '{args.output}': {error}",
                  file=sys.stderr)
            sys.exit(1)
if __name__ == "__main__":
    main()