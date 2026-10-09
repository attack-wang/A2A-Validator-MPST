'''
main.py
Entry point for the Budget Tracker application. Initializes the
command-line interface and starts the main event loop.
'''
import sys
from cli import BudgetTrackerCLI
def main():
    """Create and run the budget tracker CLI application."""
    try:
        app = BudgetTrackerCLI()
        app.run()
    except KeyboardInterrupt:
        print("\nInterrupted. Goodbye!")
        sys.exit(0)
if __name__ == "__main__":
    main()