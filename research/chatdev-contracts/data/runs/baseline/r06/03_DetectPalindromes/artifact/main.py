'''
main.py
Entry point for the palindrome detector application.
Wires together FileHandler, PalindromeDetector, and ReportGenerator and
exposes every feature (input file, detection mode, case/punctuation/
min-length settings, console + optional file report) via the command line.
Usage:
    python main.py sample_text.txt
    python main.py sample_text.txt -o report.txt
    python main.py sample_text.txt -m words --case-sensitive --min-length 4
'''
import argparse
import sys
from file_handler import FileHandler
from palindrome_detector import DetectionSettings, PalindromeDetector
from report_generator import ReportGenerator
def parse_args(argv=None):
    """Parse command-line arguments and return the parsed namespace."""
    parser = argparse.ArgumentParser(
        description="Detect palindromes in a given text file."
    )
    parser.add_argument("input_file", help="Path to the text file to scan")
    parser.add_argument("-o", "--output", default=None,
                        help="Optional path to save the report as a text file")
    parser.add_argument("-m", "--mode", choices=("words", "lines", "both"),
                        default="both", help="Detection mode (default: both)")
    parser.add_argument("--case-sensitive", action="store_true",
                        help="Do not ignore letter case when checking")
    parser.add_argument("--keep-punctuation", action="store_true",
                        help="Do not strip punctuation/spacing when normalizing")
    parser.add_argument("--min-length", type=int, default=3,
                        help="Minimum normalized length to consider (default: 3)")
    return parser.parse_args(argv)
def main(argv=None):
    """Run the full detection pipeline and return a process exit code."""
    args = parse_args(argv)
    if args.min_length < 1:
        print("Error: --min-length must be a positive integer.", file=sys.stderr)
        return 1
    settings = DetectionSettings(
        case_sensitive=args.case_sensitive,
        ignore_punctuation=not args.keep_punctuation,
        min_length=args.min_length,
    )
    try:
        text = FileHandler().read_file(args.input_file)
    except (FileNotFoundError, IsADirectoryError,
            PermissionError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    results = PalindromeDetector(settings).detect(text, mode=args.mode)
    reporter = ReportGenerator()
    reporter.print_console_report(results, source=args.input_file)
    if args.output:
        try:
            reporter.save_file_report(results, args.output,
                                      source=args.input_file)
        except OSError as exc:
            print(f"Error writing report file: {exc}", file=sys.stderr)
            return 1
    return 0
if __name__ == "__main__":
    sys.exit(main())