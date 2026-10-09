'''
main.py
Command-line entry point for the palindrome detector.
Parses command-line arguments, reads the target text file (or the built-in
demo text), runs the PalindromeDetector, prints the generated report, and
optionally saves it to an output file.
'''
import sys
import argparse
from palindrome_detector import PalindromeDetector
from report_generator import ReportGenerator
from file_handler import FileHandler, FileHandlerError
DEMO_TEXT = (
    "Madam, I'm Adam.\n"
    "A man, a plan, a canal: Panama!\n"
    "Was it a car or a cat I saw?\n"
    "This line contains no palindrome at all.\n"
    "Racecar level kayak noon.\n"
)
def parse_arguments(argv=None):
    """Parse CLI flags used by build_detector() and run()."""
    parser = argparse.ArgumentParser(description="Detect palindromes in a text file.")
    parser.add_argument("filepath", nargs="?", default=None, help="Text file to scan")
    parser.add_argument("--demo", action="store_true", help="Use built-in demo text")
    parser.add_argument("--encoding", default=None, help="Input file encoding")
    parser.add_argument("--case-sensitive", action="store_true", help="Keep letter case")
    parser.add_argument("--keep-punctuation", action="store_true", help="Keep punctuation")
    parser.add_argument("--min-length", type=int, default=2, help="Min normalized length")
    parser.add_argument("--max-phrase-words", type=int, default=6, help="Max words per phrase")
    parser.add_argument("--no-phrases", action="store_true", help="Disable phrase detection")
    parser.add_argument("--limit", type=int, default=20, help="Max matches listed per section")
    parser.add_argument("--output", default=None, help="Path to save the report")
    return parser.parse_args(argv)
def build_detector(args):
    """Create a PalindromeDetector configured from parsed CLI arguments."""
    return PalindromeDetector(
        ignore_case=not args.case_sensitive,
        ignore_non_alphanumeric=not args.keep_punctuation,
        min_length=max(1, args.min_length),
        max_phrase_words=max(2, args.max_phrase_words),
        find_phrases=not args.no_phrases,
    )
def run(args):
    """Execute the detection pipeline and return a process exit code."""
    detector = build_detector(args)
    reporter = ReportGenerator()
    file_handler = FileHandler()
    if args.demo:
        source_name = "<built-in demo text>"
        text = DEMO_TEXT
    else:
        if not args.filepath:
            print("Error: a file path is required (or use --demo).", file=sys.stderr)
            return 2
        source_name = args.filepath
        try:
            text = file_handler.read_text(args.filepath, encoding=args.encoding)
        except FileHandlerError as exc:
            print("Error: {}".format(exc), file=sys.stderr)
            return 2
    word_matches, phrase_matches, stats = detector.detect(text)
    settings = {
        "ignore_case": detector.ignore_case,
        "ignore_non_alphanumeric": detector.ignore_non_alphanumeric,
        "min_length": detector.min_length,
        "max_phrase_words": detector.max_phrase_words,
        "phrase_detection": detector.find_phrases,
    }
    report = reporter.build_report(
        source_name, word_matches, phrase_matches, stats, settings, max_listed=args.limit)
    print(report)
    if args.output:
        try:
            file_handler.write_text(args.output, report)
            print("Full report saved to: {}".format(args.output))
        except FileHandlerError as exc:
            print("Warning: {}".format(exc), file=sys.stderr)
            return 3
    return 0
def main(argv=None):
    """Program entry point; parse arguments and run the pipeline."""
    args = parse_arguments(argv)
    return run(args)
if __name__ == "__main__":
    sys.exit(main())