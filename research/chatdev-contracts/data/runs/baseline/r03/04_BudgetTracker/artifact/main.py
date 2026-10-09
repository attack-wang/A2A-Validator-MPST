'''
main.py
Entry point for the Budget Tracker application.
Run this file to launch the Budget Tracker GUI.
'''
import tkinter as tk
from gui import BudgetTrackerApp
def main():
    app = BudgetTrackerApp()
    app.mainloop()
if __name__ == "__main__":
    main()