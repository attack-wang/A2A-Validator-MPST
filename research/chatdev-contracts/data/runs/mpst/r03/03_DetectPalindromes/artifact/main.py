'''
main.py
Entry point for the Palindrome Detector application.
Dispatches to the GUI (default or with --gui/-g) or to the CLI.
'''
import sys
from cli import run_cli
def main(argv=None):
    """
    Execute the application.
    Args:
        argv (list[str] | None): Raw command-line arguments (without the
            program name). Defaults to sys.argv[1:] when None.
    Returns:
        int: Process exit code (0 on success, 1 on failure).
    """
    if argv is None:
        argv = sys.argv[1:]
    if not argv or argv[0] in ('--gui', '-g'):
        try:
            from gui import launch_gui
            launch_gui()
            return 0
        except ImportError as error:
            print("GUI could not be started:", error, file=sys.stderr)
            print("Use the command line instead: python main.py <file.txt>", file=sys.stderr)
            return 1
    return run_cli(argv)
if __name__ == '__main__':
    sys.exit(main())