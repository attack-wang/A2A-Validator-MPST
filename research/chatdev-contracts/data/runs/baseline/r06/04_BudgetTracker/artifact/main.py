'''
main.py
Entry point for the budget tracker application.
Launches the tkinter GUI defined in gui.py.
'''
import tkinter as tk
from gui import BudgetTrackerGUI
def main():
    root = tk.Tk()
    app = BudgetTrackerGUI(root)
    root.mainloop()
if __name__ == "__main__":
    main()