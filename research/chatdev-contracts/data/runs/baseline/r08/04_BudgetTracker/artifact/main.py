'''
main.py
Entry point for the Budget Tracker application.
Run with:  python main.py
'''
from gui import BudgetTrackerApp
def main():
    app = BudgetTrackerApp()
    app.mainloop()
if __name__ == "__main__":
    main()