'''
main.py
Entry point of the Palindrome Detector application.
This program reads a text file, detects palindromic words and phrases,
and prints a report to the console (optionally saving it to a file).
Usage:
    python main.py <input_file> [--min-length N] [--max-phrase-words N]
                   [--case-sensitive] [--save-report <output_file>]
'''
import argparse
import os
import sys
from file_reader import FileReader
from palindrome_detector import PalindromeDetector
from report_generator import ReportGenerator
def parse_arguments(argv=None):
    '''
    Parse command-line arguments.
    :param argv: argument list (defaults to sys.argv)
    :return: parsed arguments namespace
    '''
    parser = argparse.ArgumentParser(
        description='Detect palindromes (words and phrases) in a text file.'
    )
    parser.add_argument(
        'input_file',
        help='Path to the text file to analyze.'
    )
    parser.add_argument(
        '--min-length',
        type=int,
        default=2,
        help='Minimum character length for a palindrome (default: 2).'
    )
    parser.add_argument(
        '--max-phrase-words',
        type=int,
        default=10,
        help='Maximum number of words in a phrase to check (default: 10).'
    )
    parser.add_argument(
        '--case-sensitive',
        action='store_true',
        help='Perform case-sensitive palindrome comparison.'
    )
    parser.add_argument(
        '--save-report',
        metavar='OUTPUT_FILE',
        default=None,
        help='Optional path to save the report as a text file.'
    )
    return parser.parse_args(argv)
def run_detection(input_file, min_length, max_phrase_words, case_sensitive):
    '''
    Execute the palindrome detection pipeline on the given file.
    :param input_file: path to the input text file
    :param min_length: minimum palindrome length
    :param max_phrase_words: maximum phrase length in words
    :param case_sensitive: whether comparison is case-sensitive
    :return: tuple (results, report_text, report_generator)
    '''
    reader = FileReader()
    content = reader.read_file(input_file)
    detector = PalindromeDetector(
        min_length=min_length,
        max_phrase_words=max_phrase_words,
        case_sensitive=case_sensitive
    )
    results = detector.detect(content)
    generator = ReportGenerator(source_name=os.path.basename(input_file))
    report = generator.generate_report(results)
    return results, report, generator
def main():
    '''
    Main entry point of the application.
    '''
    args = parse_arguments()
    try:
        _, report, report_generator = run_detection(
            input_file=args.input_file,
            min_length=args.min_length,
            max_phrase_words=args.max_phrase_words,
            case_sensitive=args.case_sensitive
        )
    except (FileNotFoundError, PermissionError, ValueError) as error:
        print(f'Error: {error}', file=sys.stderr)
        sys.exit(1)
    report_generator.print_report(report)
    if args.save_report:
        saved_path = report_generator.save_report(report, args.save_report)
        print(f'Report saved to: {saved_path}')
if __name__ == '__main__':
    main()