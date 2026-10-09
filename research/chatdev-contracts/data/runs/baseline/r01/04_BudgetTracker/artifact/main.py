'''
main.py
Entry point for the ChatDev Budget Tracker application.
Launches the Tkinter GUI.
'''
import sys
from gui import BudgetTrackerApp
def main():
    try:
        app = BudgetTrackerApp()
        app.mainloop()
    except Exception as exc:
        # Fallback error reporting when the GUI cannot start
        print(f"Failed to start Budget Tracker: {exc}", file=sys.stderr)
        raise
if __name__ == "__main__":
    main()