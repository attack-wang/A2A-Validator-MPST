'''
budgettrackerapp.py
Compatibility module that exposes the main application window.
The full implementation lives in gui.py; this module simply re-exports
BudgetTrackerApp so that `main.py` (and any external code) can import it
from either location.
'''
from gui import BudgetTrackerApp
__all__ = ["BudgetTrackerApp"]