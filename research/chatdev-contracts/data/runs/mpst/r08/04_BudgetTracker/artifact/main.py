'''
Main entry point for the Budget Tracker application.
This module initializes the Tkinter root window, instantiates the
BudgetTrackerApp GUI, and starts the main event loop.
'''
import tkinter as tk
from gui import BudgetTrackerApp
def main():
    """Create the root window and launch the Budget Tracker application."""
    root = tk.Tk()
    app = BudgetTrackerApp(root)
    root.mainloop()
if __name__ == "__main__":
    main()