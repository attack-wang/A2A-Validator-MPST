'''
main.py
Entry point for the Palindrome Detector command-line application.
The tool reads a text file supplied by the user, analyzes it for
palindromic words and sentences, and prints a formatted report. The report
can optionally be saved to an output file. The input file encoding is
configurable so legacy files (e.g. cp1252 or latin-1) are handled gracefully
instead of crashing with an unhandled UnicodeDecodeError.
Usage examples:
    python main.py sample_input.txt
    python main.py sample_input.txt --output report.txt
    python main.py sample_input.txt --case-sensitive --min-length 3
    python main.py legacy_input.txt --encoding cp1252
'''
import argparse
import sys
from file_handler import FileHandler
from palindrome_detector import PalindromeDetector
from reporter import ResultReporter
def parse_arguments(argv=None):
    """
    Parse and validate command-line arguments.
    :param argv: Argument list to parse (defaults to sys.argv[1:]).
    :return: Parsed arguments namespace.
    """
    parser = argparse.ArgumentParser(
        prog='palindrome_detector',
        description='Detect palindromic words and sentences in a text file.'
    )
    parser.add_argument(
        'input_file',
        help='Path to the text file to analyze.'
    )
    parser.add_argument(
        '-o', '--output',
        default=None,
        help='Optional path to save the report as a text file.'
    )
    parser.add_argument(
        '-e', '--encoding',
        default='utf-8',
        help='Text encoding of the input file (default: utf-8). '
             'Use e.g. cp1252 or latin-1 for legacy files.'
    )
    parser.add_argument(
        '--case-sensitive',
        action='store_true',
        help='Treat uppercase and lowercase letters as different characters.'
    )
    parser.add_argument(
        '--keep-punctuation',
        action='store_true',
        help='Keep punctuation and symbols when comparing (strict mode).'
    )
    parser.add_argument(
        '--min-length',
        type=int,
        default=1,
        help='Minimum normalized length of a palindrome candidate '
             '(default: 1).'
    )
    return parser.parse_args(argv)
def run(args):
    """
    Execute the complete detection workflow.
    :param args: Parsed command-line arguments.
    :return: Process exit code (0 on success, 1 on failure).
    """
    try:
        text = FileHandler.read_text_file(args.input_file, encoding=args.encoding)
    except FileNotFoundError:
        print(f'Error: file not found: {args.input_file}', file=sys.stderr)
        return 1
    except UnicodeDecodeError:
        print(
            f'Error: could not decode "{args.input_file}" as {args.encoding}. '
            f'The file may use a different encoding; try re-running with '
            f'the --encoding option (e.g. --encoding cp1252).',
            file=sys.stderr
        )
        return 1
    except OSError as exc:
        print(f'Error: could not read file: {exc}', file=sys.stderr)
        return 1
    detector = PalindromeDetector(
        ignore_case=not args.case_sensitive,
        ignore_punctuation=not args.keep_punctuation,
        min_length=args.min_length
    )
    analysis = detector.analyze(text)
    reporter = ResultReporter(source_name=args.input_file)
    reporter.print_report(analysis)
    if args.output:
        try:
            reporter.save_report(analysis, args.output)
            print(f'Report saved to: {args.output}')
        except OSError as exc:
            print(f'Error: could not write report: {exc}', file=sys.stderr)
            return 1
    return 0
def main():
    """Application entry point: parse arguments and run the workflow."""
    arguments = parse_arguments()
    sys.exit(run(arguments))
if __name__ == '__main__':
    main()