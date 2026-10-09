'''
Entry point for the Palindrome Detector application.
Wires together file reading, palindrome detection, and report generation.
'''
import argparse
import os
import sys
from config import (DEFAULT_CASE_SENSITIVE, DEFAULT_IGNORE_NON_ALPHANUMERIC,
                    DEFAULT_MIN_WORD_LENGTH, DEFAULT_DETECT_PHRASES,
                    DEFAULT_MAX_PHRASE_WORDS, DEFAULT_DETECT_LINES)
from file_reader import read_text_file, FileReadError
from palindrome_detector import PalindromeDetector
from report_generator import generate_report, print_report, save_report
SAMPLE_TEXT = """Palindrome Detector - Sample Text
=================================
A man, a plan, a canal: Panama!
Was it a car or a cat I saw?
Never odd or even
Rats live on no evil star
Step on no pets
Madam, in Eden, I'm Adam
This line contains the words noon, radar, and civic.
Programming is fun, but level checking is cooler.
The quick brown fox jumps over the lazy dog.
12321 is a numeric palindrome.
Hello world, this is a normal sentence.
"""
def ensure_sample_file(filepath):
    '''Create a demonstration sample text file for first-run convenience.'''
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(SAMPLE_TEXT)
def build_parser():
    '''Build and return the CLI argument parser.'''
    parser = argparse.ArgumentParser(
        prog='palindrome_detector',
        description='Detect palindromes (words, phrases, whole lines) in a text file.')
    parser.add_argument('filepath', nargs='?', default='sample_text.txt',
                        help='Path to the text file to analyze (default: sample_text.txt)')
    parser.add_argument('--case-sensitive', action='store_true',
                        default=DEFAULT_CASE_SENSITIVE,
                        help='Perform case-sensitive comparison')
    parser.add_argument('--keep-non-alphanumeric', action='store_true',
                        default=not DEFAULT_IGNORE_NON_ALPHANUMERIC,
                        help='Do not strip punctuation/whitespace before comparing')
    parser.add_argument('--min-word-length', type=int, default=DEFAULT_MIN_WORD_LENGTH,
                        help='Minimum normalized length for a match')
    parser.add_argument('--no-phrases', action='store_true',
                        default=not DEFAULT_DETECT_PHRASES,
                        help='Disable phrase-level detection')
    parser.add_argument('--max-phrase-words', type=int, default=DEFAULT_MAX_PHRASE_WORDS,
                        help='Maximum words in a candidate phrase')
    parser.add_argument('--no-line-mode', action='store_true',
                        default=not DEFAULT_DETECT_LINES,
                        help='Disable whole-line palindrome detection')
    parser.add_argument('--output', metavar='FILE', default=None,
                        help='Also save the report to this file')
    return parser
def main(argv=None):
    '''CLI entry point. Returns a process exit code.'''
    args = build_parser().parse_args(argv)
    # Auto-create the sample file on first run for demonstration
    if args.filepath == 'sample_text.txt' and not os.path.exists(args.filepath):
        try:
            ensure_sample_file(args.filepath)
            print(f"[info] Sample file '{args.filepath}' was not found and has been created for demonstration.")
        except OSError as e:
            print(f"[warn] Could not create sample file '{args.filepath}': {e}")
    # Read input (graceful error handling instead of a traceback)
    try:
        text = read_text_file(args.filepath)
    except FileReadError as e:
        print(f"[error] {e}", file=sys.stderr)
        return 1
    # Run detection with user-selected settings
    detector = PalindromeDetector(
        case_sensitive=args.case_sensitive,
        ignore_non_alphanumeric=not args.keep_non_alphanumeric,
        min_word_length=args.min_word_length,
        detect_phrases=not args.no_phrases,
        max_phrase_words=args.max_phrase_words,
        detect_lines=not args.no_line_mode,
    )
    matches = detector.detect(text)
    settings_summary = (f"case_sensitive={detector.case_sensitive}, "
                        f"ignore_non_alphanumeric={detector.ignore_non_alphanumeric}, "
                        f"min_word_length={detector.min_word_length}, "
                        f"detect_phrases={detector.detect_phrases}, "
                        f"max_phrase_words={detector.max_phrase_words}, "
                        f"detect_lines={detector.detect_lines}")
    report = generate_report(matches, args.filepath, settings_summary)
    # Output: to file (if requested, with stdout fallback on failure) and/or stdout
    if args.output:
        try:
            save_report(report, args.output)
            print(f"Report saved to '{args.output}'.")
        except OSError as e:
            print(f"[error] Could not write report to '{args.output}': {e}", file=sys.stderr)
            print_report(report)
            return 1
    else:
        print_report(report)
    return 0
if __name__ == '__main__':
    sys.exit(main())