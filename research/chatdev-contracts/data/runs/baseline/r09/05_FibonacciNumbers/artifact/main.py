'''
main.py
Entry point for the Fibonacci Number Generator application.
Supports two modes of operation:
1. Non-interactive mode: pass the upper limit as a command-line
   argument (e.g., `python main.py 100`) and the results are
   printed directly - suitable for automated/headless test
   environments where stdin is closed or empty.
2. Interactive mode: launched with no arguments, starts the
   command-line interface so the user can enter limits interactively.
'''
import sys
from fibonacci import generate_fibonacci, validate_limit
from cli import run_cli, display_results
if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            # Non-interactive mode: use the command-line argument as the limit.
            try:
                limit = validate_limit(sys.argv[1])
            except ValueError as error:
                print(f"Error: {error}")
                sys.exit(1)
            display_results(generate_fibonacci(limit), limit)
        else:
            # Interactive mode: no arguments provided, run the CLI loop.
            run_cli()
    except KeyboardInterrupt:
        print("\nInterrupted by user. Goodbye!")
        sys.exit(0)