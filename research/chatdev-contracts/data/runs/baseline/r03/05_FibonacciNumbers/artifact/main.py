'''
main.py
Entry point for the Fibonacci Number Generator application.
Usage:
    python main.py                 # interactive mode
    python main.py --limit 100     # direct mode
    python main.py -l 1000         # short flag
Exit codes:
    0 - success
    1 - invalid input supplied in direct mode
'''
import sys
from cli import build_parser, run_interactive_mode, run_with_limit
def main(argv=None) -> int:
    """
    Application entry point.
    Args:
        argv: Command-line arguments; defaults to sys.argv[1:] when None.
    Returns:
        Process exit code: 0 on success, 1 on failure.
    """
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.limit is not None:
        # Direct mode: a limit was supplied on the command line.
        return 0 if run_with_limit(args.limit) else 1
    # No limit supplied: fall back to interactive mode.
    run_interactive_mode()
    return 0
if __name__ == "__main__":
    sys.exit(main())