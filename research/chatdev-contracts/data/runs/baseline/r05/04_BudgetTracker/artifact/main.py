'''
main.py
Entry point for the Budget Tracker application.
Initializes the root tkinter window and starts the GUI event loop.
'''
import tkinter as tk
from gui import BudgetTrackerApp
def main():
    """Create the main window and launch the Budget Tracker application."""
    root = tk.Tk()
    app = BudgetTrackerApp(root)
    root.mainloop()
if __name__ == "__main__":
    main()