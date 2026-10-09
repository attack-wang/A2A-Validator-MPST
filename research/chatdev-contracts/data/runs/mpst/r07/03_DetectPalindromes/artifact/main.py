'''
main.py - Entry point of the Palindrome Detector application.
This command-line application reads a text file, detects palindromes at
the word, sentence/phrase, and (optionally) substring level, prints a
formatted report to the console, and can optionally save the report to
an output file.
Usage examples:
    python main.py sample_text.txt
    python main.py sample_text.txt --substrings --output report.txt
    python main.py sample_text.txt --min-word-length 4 --case-sensitive
'''
import argparse
import sys
from file_handler import FileHandler
from palindrome_detector import PalindromeDetector
from report_generator import ReportGenerator
def parse_arguments(argv=None):
    """Parse and return command-line arguments."""
    parser = argparse.ArgumentParser(
        prog="palindrome-detector",
        description="Detect palindromes (words, sentences/phrases, and "
                    "substrings) inside a given text file.",
        epilog="Example: python main.py sample_text.txt --substrings -o report.txt",
    )
    parser.add_argument(
        "file",
        help="Path to the text file to analyze.",
    )
    parser.add_argument(
        "--min-word-length",
        type=int,
        default=3,
        help="Minimum length (in characters) for a word to be considered. "
             "Default: 3.",
    )
    parser.add_argument(
        "--min-sentence-length",
        type=int,
        default=3,
        help="Minimum normalized length for a sentence/phrase to be "
             "considered. Default: 3.",
    )
    parser.add_argument(
        "--min-substring-length",
        type=int,
        default=3,
        help="Minimum length for palindromic substrings (used only with "
             "--substrings). Default: 3.",
    )
    parser.add_argument(
        "--substrings",
        action="store_true",
        help="Also search for palindromic substrings (slower on very large "
             "files).",
    )
    parser.add_argument(
        "--case-sensitive",
        action="store_true",
        help="Treat uppercase and lowercase letters as different "
             "(palindrome check becomes case-sensitive).",
    )
    parser.add_argument(
        "-o", "--output",
        help="Optional path to save the generated report as a text file.",
    )
    return parser.parse_args(argv)
def run_analysis(args):
    """Load the file, run detection, print (and optionally save) the report."""
    print(f"Reading file: {args.file}")
    content = FileHandler.read_text_file(args.file)
    print(f"Read {len(content)} characters. Analyzing...")
    detector = PalindromeDetector(case_sensitive=args.case_sensitive)
    results = detector.analyze(
        content,
        min_word_length=args.min_word_length,
        min_sentence_length=args.min_sentence_length,
        min_substring_length=args.min_substring_length,
        include_substrings=args.substrings,
    )
    report = ReportGenerator(source_name=args.file).generate_report(results)
    print(report)
    if args.output:
        FileHandler.write_text_file(args.output, report)
        print(f"\nReport saved to: {args.output}")
def main(argv=None):
    """Application entry point. Returns a process exit code."""
    args = parse_arguments(argv)
    try:
        run_analysis(args)
    except FileNotFoundError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    except IsADirectoryError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nInterrupted by user.", file=sys.stderr)
        return 130
    return 0
if __name__ == "__main__":
    sys.exit(main())