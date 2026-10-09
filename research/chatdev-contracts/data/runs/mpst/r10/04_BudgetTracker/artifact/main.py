'''
Main entry point for the Budget Tracker application.
Launches the Tkinter GUI application.
'''
import tkinter as tk
from gui import BudgetTrackerApp
def main():
    root = tk.Tk()
    app = BudgetTrackerApp(root)
    root.mainloop()
if __name__ == "__main__":
    main()