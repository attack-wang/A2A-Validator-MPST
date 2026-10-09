'''
main.py
Entry point for the Palindrome Detector application.
Usage:
    python main.py sample_text.txt
    python main.py sample_text.txt --mode sentences --min-length 3
    python main.py sample_text.txt --output report.txt --unique
'''
import argparse
import sys
from file_reader import FileReader
from palindrome_detector import PalindromeDetector
from report_generator import ReportGenerator
def parse_arguments(argv=None) -> argparse.Namespace:
    """Parse command-line arguments and return the configuration."""
    parser = argparse.ArgumentParser(
        description="Detect palindromes in a given text file.")
    parser.add_argument("input_file", help="Path to the text file to scan")
    parser.add_argument("--mode", choices=("words", "sentences"),
                        default="words",
                        help="Scan individual words or whole sentences (default: words)")
    parser.add_argument("--min-length", type=int, default=2,
                        help="Minimum normalized palindrome length (default: 2)")
    parser.add_argument("--case-sensitive", action="store_true",
                        help="Treat upper- and lower-case letters as different")
    parser.add_argument("--keep-punctuation", action="store_true",
                        help="Do NOT strip punctuation/whitespace before comparing")
    parser.add_argument("--unique", action="store_true",
                        help="Collapse duplicate palindromes so each appears once")
    parser.add_argument("--no-details", action="store_true",
                        help="Hide per-match details (line, offset, length)")
    parser.add_argument("--output", default=None,
                        help="Optional path to save the report as a text file")
    return parser.parse_args(argv)
def run(args: argparse.Namespace) -> int:
    """Execute one full detection run. Returns a process exit code."""
    # 1. Build the detector (validates min_length).
    try:
        detector = PalindromeDetector(
            min_length=args.min_length,
            case_sensitive=args.case_sensitive,
            ignore_punctuation=not args.keep_punctuation,
        )
    except ValueError as error:
        print("ERROR: {0}".format(error), file=sys.stderr)
        return 1
    # 2. Read the input file with robust encoding handling.
    try:
        text = FileReader().read(args.input_file)
    except (FileNotFoundError, IsADirectoryError, ValueError, OSError) as error:
        print("ERROR: {0}".format(error), file=sys.stderr)
        return 1
    # 3. Detect palindromes in the requested mode.
    try:
        matches = detector.detect(text, mode=args.mode)
    except ValueError as error:
        print("ERROR: {0}".format(error), file=sys.stderr)
        return 1
    if args.unique:
        matches = detector.unique_matches(matches)
    # 4. Build, print, and optionally save the report.
    generator = ReportGenerator(show_details=not args.no_details)
    report = generator.format_report(
        matches=matches,
        source_file=args.input_file,
        mode=args.mode,
        stats=detector.last_scan_stats,
    )
    generator.print_report(report)
    if args.output:
        try:
            generator.save_report(report, args.output)
            print("Report saved to: {0}".format(args.output))
        except OSError as error:
            print("ERROR: could not save report: {0}".format(error), file=sys.stderr)
            return 1
    return 0
def main() -> None:
    """Program entry point."""
    sys.exit(run(parse_arguments()))
if __name__ == "__main__":
    main()