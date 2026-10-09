'''
main.py
Command-line entry point for the Palindrome Detector application.
Usage examples:
    python main.py input.txt
    python main.py input.txt --mode phrase --min-length 3
    python main.py input.txt --mode all --case-sensitive --output results.txt
'''
import argparse
import os
import sys
from file_handler import FileHandler
from palindrome_detector import PalindromeDetector
from report_generator import ReportGenerator
VALID_MODES = ('word', 'phrase', 'line', 'all')
def build_argument_parser():
    """Create and return the configured argparse parser."""
    parser = argparse.ArgumentParser(
        prog='palindrome_detector',
        description='Detect palindromes in a given text file.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        'input_file',
        help='Path to the text file that should be scanned.',
    )
    parser.add_argument(
        '-m', '--mode',
        choices=VALID_MODES,
        default='word',
        help='Detection granularity: individual words, whole phrases/sentences, '
             'entire lines, or all of them combined.',
    )
    parser.add_argument(
        '-o', '--output',
        default=None,
        help='Optional path to a report file. When omitted, results are only '
             'printed to the console.',
    )
    parser.add_argument(
        '--case-sensitive',
        action='store_true',
        help='Treat uppercase and lowercase letters as different characters.',
    )
    parser.add_argument(
        '--keep-punctuation',
        action='store_true',
        help='Do NOT strip punctuation and whitespace before comparing '
             '(strict character-by-character comparison).',
    )
    parser.add_argument(
        '--min-length',
        type=int,
        default=3,
        help='Minimum number of characters (after normalization) a fragment '
             'must have to be considered a palindrome.',
    )
    parser.add_argument(
        '--encoding',
        default='utf-8',
        help='Text encoding used to read the input file.',
    )
    return parser
def run_detection(args):
    """Execute the full detect-and-report pipeline; returns exit code."""
    try:
        text = FileHandler.read_file(args.input_file, encoding=args.encoding)
    except (FileNotFoundError, PermissionError, ValueError, OSError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 1
    detector = PalindromeDetector(
        case_insensitive=not args.case_sensitive,
        ignore_punctuation=not args.keep_punctuation,
        min_length=args.min_length,
    )
    matches = detector.detect(text, mode=args.mode)
    stats = PalindromeDetector.build_statistics(
        matches=matches,
        mode=args.mode,
        source_name=os.path.basename(args.input_file),
        total_lines=len(text.splitlines()),
        total_characters=len(text),
    )
    report = ReportGenerator.generate_console_report(matches, stats)
    print(report)
    if args.output:
        file_report = ReportGenerator.generate_text_report(matches, stats)
        try:
            FileHandler.write_file(args.output, file_report)
            print(f'\nReport saved to: {args.output}')
        except OSError as exc:
            print(f'ERROR: could not write report file: {exc}', file=sys.stderr)
            return 1
    return 0
def main(argv=None):
    """Program entry point."""
    parser = build_argument_parser()
    args = parser.parse_args(argv)
    return run_detection(args)
if __name__ == '__main__':
    sys.exit(main())