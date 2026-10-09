'''
Entry point for the Palindrome Detector application.
Parses command-line arguments, reads the input text file, runs palindrome
detection, displays a human-readable report on the console, and optionally
saves the report to an output file.
Usage:
    python main.py sample_text.txt
    python main.py sample_text.txt -o report.txt
    python main.py sample_text.txt --case-sensitive --min-length 3
'''
import argparse
import sys
from file_handler import FileHandlerError, read_text_file, write_results_to_file
from palindrome_detector import PalindromeDetector
from report_generator import display_report, generate_report
def parse_arguments(argv=None):
    """Parse and return command-line arguments."""
    parser = argparse.ArgumentParser(
        prog="palindrome_detector",
        description="Detect palindromic words, phrases, and lines in a text file.",
    )
    parser.add_argument(
        "input_file",
        help="Path to the text file to analyze.",
    )
    parser.add_argument(
        "-o", "--output",
        default=None,
        help="Optional path to save the generated report as a text file.",
    )
    parser.add_argument(
        "-m", "--min-length",
        type=int,
        default=2,
        help="Minimum normalized length for a candidate (default: 2).",
    )
    parser.add_argument(
        "--case-sensitive",
        action="store_true",
        help="Do not ignore letter case when checking candidates.",
    )
    parser.add_argument(
        "--keep-punctuation",
        action="store_true",
        help="Do not strip punctuation before checking (mainly affects whole-line "
             "detection; whitespace is still ignored).",
    )
    parser.add_argument(
        "--max-phrase-words",
        type=int,
        default=10,
        help="Maximum number of words in a phrase candidate (default: 10).",
    )
    parser.add_argument(
        "--encoding",
        default="utf-8",
        help="Text encoding of the input file (default: utf-8).",
    )
    return parser.parse_args(argv)
def run_detection(args):
    """Execute the detection pipeline and return the formatted report."""
    text = read_text_file(args.input_file, encoding=args.encoding)
    detector = PalindromeDetector(
        min_length=args.min_length,
        case_insensitive=not args.case_sensitive,
        ignore_punctuation=not args.keep_punctuation,
    )
    results = detector.detect(text, max_phrase_words=args.max_phrase_words)
    return generate_report(results, source_file=args.input_file)
def main(argv=None):
    """Application entry point. Returns a process exit code."""
    args = parse_arguments(argv)
    try:
        report = run_detection(args)
    except FileHandlerError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    display_report(report)
    if args.output:
        try:
            write_results_to_file(report, args.output, encoding=args.encoding)
            print(f"\nReport saved to: {args.output}")
        except FileHandlerError as error:
            print(f"Error: could not save report: {error}", file=sys.stderr)
            return 1
    return 0
if __name__ == "__main__":
    sys.exit(main())