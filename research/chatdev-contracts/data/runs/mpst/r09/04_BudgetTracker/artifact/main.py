'''
main.py
Entry point for the Budget Tracker application.
Launches the tkinter main window. Run this file directly:
    python main.py
'''
import tkinter as tk
from budgettrackerapp import BudgetTrackerApp
def main():
    """Create the root window and start the application event loop."""
    root = tk.Tk()
    app = BudgetTrackerApp(root)
    root.mainloop()
    return app
if __name__ == "__main__":
    main()