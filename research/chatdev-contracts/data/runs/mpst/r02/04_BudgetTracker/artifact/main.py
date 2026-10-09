import tkinter as tk
from database import Database
from gui import BudgetTrackerApp
def main():
    root = tk.Tk()
    db = Database("budget_tracker.db")
    app = BudgetTrackerApp(root, db)
    root.mainloop()
if __name__ == "__main__":
    main()