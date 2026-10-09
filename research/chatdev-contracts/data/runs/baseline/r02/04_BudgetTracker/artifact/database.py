"""
database.py
Persistence layer for the Budget Tracker application.
Uses an SQLite database file stored next to the application (by default
`budget_tracker.db`) so that all transactions, categories and savings
goals survive across sessions.
Public API (Database class):
- add_transaction / update_transaction / delete_transaction
- get_transactions (with optional date / category / type filters)
- get_categories / add_category / delete_category
- add_savings_goal / delete_savings_goal / get_savings_goals
- get_totals (income / expense / savings totals, optionally for a period)
"""
import sqlite3
from datetime import datetime
from typing import Iterable, List, Optional, Tuple
from models import Transaction, SavingsGoal, TRANSACTION_EXPENSE, TRANSACTION_INCOME
DEFAULT_DB_PATH = "budget_tracker.db"
DEFAULT_CATEGORIES = (
    ("Food", TRANSACTION_EXPENSE),
    ("Housing", TRANSACTION_EXPENSE),
    ("Transport", TRANSACTION_EXPENSE),
    ("Utilities", TRANSACTION_EXPENSE),
    ("Entertainment", TRANSACTION_EXPENSE),
    ("Health", TRANSACTION_EXPENSE),
    ("Shopping", TRANSACTION_EXPENSE),
    ("Education", TRANSACTION_EXPENSE),
    ("Other", TRANSACTION_EXPENSE),
    ("Salary", TRANSACTION_INCOME),
    ("Gift", TRANSACTION_INCOME),
    ("Other Income", TRANSACTION_INCOME),
)
class Database:
    """SQLite-backed storage for transactions, categories and savings goals."""
    def __init__(self, db_path: str = DEFAULT_DB_PATH) -> None:
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()
        self._seed_default_categories()
    # ------------------------------------------------------------------ #
    # Setup
    # ------------------------------------------------------------------ #
    def _create_tables(self) -> None:
        ...
    def _seed_default_categories(self) -> None:
        ...
    def close(self) -> None:
        self.conn.close()
    # Transactions CRUD
    def add_transaction(self, date, description, amount, category, tx_type) -> int
    def update_transaction(self, tx_id, date, description, amount, category, tx_type) -> None
    def delete_transaction(self, tx_id) -> None
    def get_transaction(self, tx_id) -> Optional[Transaction]
    def get_transactions(self, start_date=None, end_date=None, category=None, tx_type=None) -> List[Transaction]
    # Categories
    def get_categories(self, tx_type=None) -> List[str]
    def add_category(self, name, tx_type) -> bool  # False if duplicate
    def delete_category(self, name) -> int  # rows deleted
    # Goals
    def add_savings_goal(self, name, target_amount) -> int
    def delete_savings_goal(self, goal_id) -> None
    def get_savings_goals(self) -> List[SavingsGoal]
    # Aggregations
    def get_totals(self, start_date=None, end_date=None) -> dict
    def get_monthly_series(self, start_date=None, end_date=None) -> List[Tuple[str, float, float]]
    def get_category_breakdown(self, start_date=None, end_date=None, tx_type=TRANSACTION_EXPENSE) -> List[Tuple[str, float]]
    def get_available_months(self) -> List[str]