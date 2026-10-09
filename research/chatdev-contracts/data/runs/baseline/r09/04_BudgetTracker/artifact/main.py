'''
main.py
Entry point for the ChatDev Budget Tracker application.
Launches the Tkinter main window defined in gui.BudgetTrackerApp.
Run with:  python main.py
'''
import tkinter as tk
from gui import BudgetTrackerApp
APP_TITLE = "ChatDev Budget Tracker"
APP_SIZE = "1060x700"
def main():
    """Create the root window, start the application, and enter the event loop."""
    root = tk.Tk()
    root.title(APP_TITLE)
    root.geometry(APP_SIZE)
    root.minsize(940, 620)
    BudgetTrackerApp(root)
    root.mainloop()
if __name__ == "__main__":
    main()