'''
main.py
Entry point for the Budget Tracker application.
Creates the BudgetTrackerApp main window and starts the Tkinter event loop.
Fix applied (per test report):
The original version referenced BudgetTrackerApp without importing it,
which raised `NameError: name 'BudgetTrackerApp' is not defined` before
the GUI could be constructed. The class is now imported from the
compatibility module `budgettrackerapp` (which re-exports it from
`gui.py`), so the application starts correctly.
'''
from budgettrackerapp import BudgetTrackerApp
def main():
    app = BudgetTrackerApp()
    app.mainloop()
if __name__ == "__main__":
    main()