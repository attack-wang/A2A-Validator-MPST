'''
main.py
Entry point for the Budget Tracker application.
Launches the Tkinter GUI. Run with: python main.py
'''
from gui import BudgetTrackerApp
if __name__ == "__main__":
    app = BudgetTrackerApp()
    app.mainloop()