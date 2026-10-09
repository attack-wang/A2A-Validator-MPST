'''
Main entry point of the Palindrome Detector application.
Parses command-line arguments, reads the input text file, runs the
detection, prints the report to the console and optionally saves it
to an output file. Returns proper process exit codes.
'''
import argparse
import sys
from config import (
    DEFAULT_MIN_LENGTH,
    DEFAULT_CASE_SENSITIVE,
    DEFAULT_INCLUDE_PHRASES,
    DEFAULT_OUTPUT_FILE,
)
from file_handler import FileHandler
from palindrome_detector import PalindromeDetector
from report_generator import ReportGenerator
def parse_arguments(argv=None):
    '''Define and parse all command-line options of the application.'''
    parser = argparse.ArgumentParser(
        description="Detect palindromic words (and optionally phrases) in a text file."
    )
    parser.add_argument("input_file", help="Path to the text file to analyse.")
    parser.add_argument("-o", "--output-file", default=DEFAULT_OUTPUT_FILE,
                        help="Optional path of a report file to write.")
    parser.add_argument("--min-length", type=int, default=DEFAULT_MIN_LENGTH,
                        help="Minimum alphanumeric length of a palindrome (default: %(default)s).")
    parser.add_argument("--case-sensitive", action="store_true",
                        default=DEFAULT_CASE_SENSITIVE,
                        help="Make the palindrome check case-sensitive.")
    parser.add_argument("--include-phrases", action="store_true",
                        default=DEFAULT_INCLUDE_PHRASES,
                        help="Also check whole lines as palindromic phrases.")
    return parser.parse_args(argv)
def main(argv=None):
    '''Run the full detection workflow; return a process exit code.'''
    arguments = parse_arguments(argv)
    # Validate options (integrates the previously orphaned fragment,
    # with the stray 'min_length' line removed).
    if arguments.min_length < 1:
        print("Error: --min-length must be a positive integer.", file=sys.stderr)
        return 1
    # Read the input file with friendly error reporting.
    try:
        text = FileHandler.read_file(arguments.input_file)
    except (FileNotFoundError, ValueError, OSError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    # Detect palindromes and compute statistics.
    detector = PalindromeDetector(
        min_length=arguments.min_length,
        case_sensitive=arguments.case_sensitive,
        include_phrases=arguments.include_phrases,
    )
    findings = detector.detect(text)
    statistics = detector.compute_statistics(findings)
    # Build and print the report.
    generator = ReportGenerator(source_name=arguments.input_file)
    report = generator.generate(findings, statistics)
    generator.print_report(report)
    # Optionally persist the report to disk.
    if arguments.output_file:
        try:
            FileHandler.write_file(arguments.output_file, report)
            print(f"Report saved to '{arguments.output_file}'.")
        except OSError as error:
            print(f"Error: {error}", file=sys.stderr)
            return 1
    return 0
if __name__ == "__main__":
    sys.exit(main())