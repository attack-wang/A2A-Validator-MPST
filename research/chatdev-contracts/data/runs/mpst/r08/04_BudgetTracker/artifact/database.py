'''
Database layer for the Budget Tracker application.
Uses SQLite to persist transactions, budgets, and savings goals.
All CRUD operations are encapsulated in the Database class.
'''
import sqlite3
from datetime import datetime
class Database:
    """Handles all SQLite database operations for the budget tracker."""
    def __init__(self, db_name="budget_tracker.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.conn.row_factory = sqlite3.Row
        self.create_tables()
    def create_tables(self):
        """Create the required tables if they do not already exist."""
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                amount REAL NOT NULL,
                transaction_type TEXT NOT NULL CHECK(transaction_type IN ('Expense', 'Income'))
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS budgets (
                category TEXT PRIMARY KEY,
                monthly_limit REAL NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS savings_goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                target_amount REAL NOT NULL,
                current_amount REAL NOT NULL DEFAULT 0,
                deadline TEXT
            )
        """)
        self.conn.commit()
    # ---------- Transactions ----------
    def add_transaction(self, date, category, description, amount, transaction_type):
        """Insert a new transaction and return its id."""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO transactions (date, category, description, amount, transaction_type) VALUES (?, ?, ?, ?, ?)",
            (date, category, description, amount, transaction_type)
        )
        self.conn.commit()
        return cursor.lastrowid
    def get_all_transactions(self):
        """Return all transactions ordered by date (newest first)."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM transactions ORDER BY date DESC, id DESC")
        return cursor.fetchall()
    def delete_transaction(self, transaction_id):
        """Delete a transaction by its id."""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
        self.conn.commit()
    def get_transactions_by_month(self, year, month):
        """Return transactions for a given year and month."""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM transactions WHERE strftime('%Y', date) = ? AND strftime('%m', date) = ? ORDER BY date DESC",
            (str(year), f"{month:02d}")
        )
        return cursor.fetchall()
    def get_expenses_by_category(self, year, month):
        """Return a dict {category: total} of expenses for a given month."""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT category, SUM(amount) as total FROM transactions WHERE transaction_type = 'Expense' AND strftime('%Y', date) = ? AND strftime('%m', date) = ? GROUP BY category",
            (str(year), f"{month:02d}")
        )
        return {row["category"]: row["total"] for row in cursor.fetchall()}
    def get_monthly_summary(self, year, month):
        """Return (total_income, total_expenses, net_savings) for a month."""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE transaction_type = 'Income' AND strftime('%Y', date) = ? AND strftime('%m', date) = ?",
            (str(year), f"{month:02d}")
        )
        income = cursor.fetchone()[0]
        cursor.execute(
            "SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE transaction_type = 'Expense' AND strftime('%Y', date) = ? AND strftime('%m', date) = ?",
            (str(year), f"{month:02d}")
        )
        expenses = cursor.fetchone()[0]
        return income, expenses, income - expenses
    def get_monthly_trend(self, months=6):
        """Return a list of (year, month, income, expenses) for the last N months."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT strftime('%Y', date) as y, strftime('%m', date) as m,
                   SUM(CASE WHEN transaction_type = 'Income' THEN amount ELSE 0 END) as income,
                   SUM(CASE WHEN transaction_type = 'Expense' THEN amount ELSE 0 END) as expenses
            FROM transactions
            GROUP BY y, m
            ORDER BY y DESC, m DESC
            LIMIT ?
        """, (months,))
        rows = cursor.fetchall()
        rows = list(reversed(rows))
        return [(row["y"], int(row["m"]), row["income"] or 0, row["expenses"] or 0) for row in rows]
    # ---------- Budgets ----------
    def set_budget(self, category, monthly_limit):
        """Insert or update the monthly budget for a category."""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO budgets (category, monthly_limit) VALUES (?, ?) ON CONFLICT(category) DO UPDATE SET monthly_limit = excluded.monthly_limit",
            (category, monthly_limit)
        )
        self.conn.commit()
    def get_budgets(self):
        """Return all budgets as a dict {category: limit}."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT category, monthly_limit FROM budgets ORDER BY category")
        return {row["category"]: row["monthly_limit"] for row in cursor.fetchall()}
    def delete_budget(self, category):
        """Delete a budget for a category."""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM budgets WHERE category = ?", (category,))
        self.conn.commit()
    # ---------- Savings Goals ----------
    def add_savings_goal(self, name, target_amount, deadline):
        """Insert a new savings goal and return its id."""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO savings_goals (name, target_amount, current_amount, deadline) VALUES (?, ?, 0, ?)",
            (name, target_amount, deadline)
        )
        self.conn.commit()
        return cursor.lastrowid
    def get_savings_goals(self):
        """Return all savings goals."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM savings_goals ORDER BY id")
        return cursor.fetchall()
    def contribute_to_goal(self, goal_id, amount):
        """Add an amount to a goal's current progress."""
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE savings_goals SET current_amount = current_amount + ? WHERE id = ?",
            (amount, goal_id)
        )
        self.conn.commit()
    def delete_savings_goal(self, goal_id):
        """Delete a savings goal by id."""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM savings_goals WHERE id = ?", (goal_id,))
        self.conn.commit()
    def close(self):
        """Close the database connection."""
        self.conn.close()