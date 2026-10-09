'''
main.py
Entry point for the Palindrome Detector application.
Reads a text file, scans it for palindromic words, lines, and
sentences, then presents the results in the console and optionally
saves them to a report file.
Usage:
    python main.py input.txt [--mode words|lines|sentences|all]
                             [--min-length N] [--case-sensitive]
                             [--keep-punctuation] [--output report.txt]
'''
import argparse
import sys
from palindrome_detector import PalindromeDetector
from file_handler import FileHandler
from report_generator import ReportGenerator
def parse_arguments(argv=None):
    '''
    Parse command-line arguments.
    Args:
        argv (list): Optional argument list (defaults to sys.argv).
    Returns:
        argparse.Namespace: Parsed arguments.
    '''
    parser = argparse.ArgumentParser(
        description='Detect palindromes in a given text file.'
    )
    parser.add_argument(
        'input_file',
        help='Path to the text file to scan for palindromes.'
    )
    parser.add_argument(
        '--mode',
        choices=['words', 'lines', 'sentences', 'all'],
        default='all',
        help='Detection mode: words, lines, sentences, or all (default: all).'
    )
    parser.add_argument(
        '--min-length',
        type=int,
        default=2,
        help='Minimum cleaned length for a palindrome (default: 2). '
             'Single-character palindromes such as "a" or "I" are excluded '
             'by default; pass --min-length 1 to include them.'
    )
    parser.add_argument(
        '--case-sensitive',
        action='store_true',
        help='Perform case-sensitive palindrome comparison.'
    )
    parser.add_argument(
        '--keep-punctuation',
        action='store_true',
        help='Do NOT strip punctuation/spaces (strict character-level check).'
    )
    parser.add_argument(
        '--output',
        default=None,
        help='Optional path to save the results report as a text file.'
    )
    return parser.parse_args(argv)
def build_statistics(text, word_results, line_results, sentence_results, mode):
    '''
    Assemble summary statistics for the scan.
    Args:
        text (str): The scanned text.
        word_results (list): Palindromic words found.
        line_results (list): Palindromic lines found.
        sentence_results (list): Palindromic sentences found.
        mode (str): The detection mode used.
    Returns:
        dict: Statistics describing the scan.
    '''
    total_words = len(text.split())
    total_lines = len([line for line in text.splitlines() if line.strip()])
    total_palindromes = 0
    if mode in ('words', 'all'):
        total_palindromes += sum(entry['count'] for entry in word_results)
    if mode in ('lines', 'all'):
        total_palindromes += len(line_results)
    if mode in ('sentences', 'all'):
        total_palindromes += len(sentence_results)
    return {
        'Detection mode': mode,
        'Total words scanned': total_words,
        'Total non-empty lines': total_lines,
        'Unique palindromic words': len(word_results),
        'Palindromic word occurrences': sum(entry['count'] for entry in word_results),
        'Palindromic lines': len(line_results),
        'Palindromic sentences': len(sentence_results),
        'Total palindromes detected': total_palindromes
    }
def run_detection(args):
    '''
    Execute the palindrome detection workflow.
    Args:
        args (argparse.Namespace): Parsed command-line arguments.
    Returns:
        int: Exit code (0 on success, 1 on failure).
    '''
    try:
        text = FileHandler.read_text(args.input_file)
    except (FileNotFoundError, IOError) as error:
        print(f'Error: {error}')
        return 1
    detector = PalindromeDetector(
        case_sensitive=args.case_sensitive,
        ignore_non_alphanumeric=not args.keep_punctuation,
        min_length=args.min_length
    )
    mode = args.mode
    word_results = detector.detect_word_palindromes(text) if mode in ('words', 'all') else []
    line_results = detector.detect_line_palindromes(text) if mode in ('lines', 'all') else []
    sentence_results = detector.detect_sentence_palindromes(text) if mode in ('sentences', 'all') else []
    stats = build_statistics(text, word_results, line_results, sentence_results, mode)
    detector_info = {
        'Input file': args.input_file,
        'Case sensitive': args.case_sensitive,
        'Ignore punctuation/spaces': not args.keep_punctuation,
        'Minimum length': args.min_length
    }
    reporter = ReportGenerator(detector_info=detector_info)
    reporter.generate_console_report(mode, word_results, line_results, sentence_results, stats)
    if args.output:
        try:
            written = reporter.generate_file_report(
                args.output, mode, word_results, line_results, sentence_results, stats
            )
            print(f"\nReport saved to: {written}")
        except IOError as error:
            print(f'Warning: Could not write report file: {error}')
    return 0
def main():
    '''
    Application entry point. Parses arguments and runs detection.
    '''
    args = parse_arguments()
    sys.exit(run_detection(args))
if __name__ == '__main__':
    main()