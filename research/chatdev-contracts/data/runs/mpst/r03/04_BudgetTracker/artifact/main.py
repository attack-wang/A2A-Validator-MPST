"""
main.py
Entry point for the Budget Tracker application.
Wires together the storage, business-logic and GUI layers and starts the
tkinter main loop. Run with:  python main.py
"""
import tkinter as tk
from budget_manager import BudgetManager
from gui import BudgetTrackerGUI
def main():
    root = tk.Tk()
    manager = BudgetManager()
    app = BudgetTrackerGUI(root, manager)
    root.mainloop()
if __name__ == "__main__":
    main()