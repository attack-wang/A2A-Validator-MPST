'''
main.py
Entry point for the Budget Tracker application.
'''
import tkinter as tk
from storage import JSONStorage
from tracker import BudgetTracker
from gui import BudgetTrackerGUI
def main():
    storage = JSONStorage("budget_data.json")
    tracker = BudgetTracker(storage)
    root = tk.Tk()
    app = BudgetTrackerGUI(root, tracker)
    root.mainloop()
if __name__ == "__main__":
    main()