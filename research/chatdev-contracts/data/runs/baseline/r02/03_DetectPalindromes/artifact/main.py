'''
main.py
Entry point for the Palindrome Detector application.
Parses command-line arguments, reads the input text file,
runs the palindrome analysis, and outputs the report to the
console and (optionally) to a report file.
'''
import argparse
import sys
from palindrome_detector import PalindromeDetector
from file_handler import FileHandler
from report_generator import ReportGenerator
def parse_arguments():
    '''
    Parse and return command-line arguments.
    :return: argparse.Namespace with user-provided options.
    '''
    parser = argparse.ArgumentParser(
        description='Detect palindromic words and phrases in a text file.'
    )
    parser.add_argument('input_file', help='Path to the text file to analyze.')
    parser.add_argument('-o', '--output', default=None,
                        help='Optional path to save the text report.')
    parser.add_argument('--case-sensitive', action='store_true',
                        help='Do not ignore letter casing when checking palindromes.')
    parser.add_argument('--keep-non-alphanumeric', action='store_true',
                        help='Do not ignore spaces/punctuation when checking palindromes.')
    parser.add_argument('--min-length', type=int, default=3,
                        help='Minimum normalized length for a token (default: 3).')
    parser.add_argument('--encoding', default='utf-8',
                        help='Text encoding of the input file (default: utf-8).')
    return parser.parse_args()
def main():
    '''
    Execute the full palindrome detection workflow:
    read file -> analyze -> print report -> optionally save report.
    '''
    args = parse_arguments()
    # Read and validate the input file with friendly error handling.
    try:
        text = FileHandler.read_file(args.input_file, encoding=args.encoding)
    except (FileNotFoundError, IOError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
    # Run the analysis with user-configurable normalization options.
    detector = PalindromeDetector(
        ignore_case=not args.case_sensitive,
        ignore_non_alphanumeric=not args.keep_non_alphanumeric,
        min_length=args.min_length,
    )
    results = detector.analyze(text)
    # Generate and display the report.
    reporter = ReportGenerator(source_filename=args.input_file)
    report = reporter.generate_report(results)
    reporter.print_report(results)
    # Optionally persist the report to disk.
    if args.output:
        try:
            FileHandler.write_file(args.output, report, encoding=args.encoding)
            print(f"\nReport saved to: {args.output}")
        except OSError as exc:
            print(f"Error writing report file: {exc}", file=sys.stderr)
            sys.exit(1)
if __name__ == '__main__':
    main()