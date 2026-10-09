"""SQLite data-access layer for the budget tracker application."""
import sqlite3
from typing import List, Optional, Tuple
from models import Transaction, Budget, SavingsGoal
class Database:
    """Handles all persistence: transactions, budgets, and savings goals."""
    def __init__(self, db_path: str = "budget_tracker.db") -> None:
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()
    def _create_tables(self) -> None:
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                type TEXT NOT NULL CHECK (type IN ('expense', 'income')),
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT NOT NULL DEFAULT ''
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
                name TEXT NOT NULL UNIQUE,
                target_amount REAL NOT NULL,
                saved_amount REAL NOT NULL DEFAULT 0,
                deadline TEXT NOT NULL DEFAULT ''
            )
        """)
        self.conn.commit()
    def close(self) -> None:
        self.conn.close()
    # ---------------- Transactions ----------------
    def add_transaction(self, date: str, tx_type: str, category: str,
                        amount: float, description: str) -> int:
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO transactions (date, type, category, amount, description) "
            "VALUES (?, ?, ?, ?, ?)",
            (date, tx_type, category, amount, description),
        )
        self.conn.commit()
        return cursor.lastrowid
    def update_transaction(self, tx_id: int, date: str, tx_type: str,
                           category: str, amount: float, description: str) -> None:
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE transactions SET date = ?, type = ?, category = ?, "
            "amount = ?, description = ? WHERE id = ?",
            (date, tx_type, category, amount, description, tx_id),
        )
        self.conn.commit()
    def delete_transaction(self, tx_id: int) -> None:
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM transactions WHERE id = ?", (tx_id,))
        self.conn.commit()
    def get_all_transactions(self) -> List[Transaction]:
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id, date, type, category, amount, description "
            "FROM transactions ORDER BY date DESC, id DESC"
        )
        return [Transaction(**dict(row)) for row in cursor.fetchall()]
    def get_transactions_by_month(self, year: int, month: int) -> List[Transaction]:
        cursor = self.conn.cursor()
        prefix = f"{year:04d}-{month:02d}"
        cursor.execute(
            "SELECT id, date, type, category, amount, description "
            "FROM transactions WHERE date LIKE ? ORDER BY date DESC, id DESC",
            (prefix + "%",),
        )
        return [Transaction(**dict(row)) for row in cursor.fetchall()]
    # ---------------- Budgets ----------------
    def set_budget(self, category: str, monthly_limit: float) -> None:
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO budgets (category, monthly_limit) VALUES (?, ?) "
            "ON CONFLICT(category) DO UPDATE SET monthly_limit = excluded.monthly_limit",
            (category, monthly_limit),
        )
        self.conn.commit()
    def get_budgets(self) -> List[Budget]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT category, monthly_limit FROM budgets ORDER BY category")
        return [Budget(**dict(row)) for row in cursor.fetchall()]
    def delete_budget(self, category: str) -> None:
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM budgets WHERE category = ?", (category,))
        self.conn.commit()
    # ---------------- Savings goals ----------------
    def add_savings_goal(self, name: str, target_amount: float, deadline: str) -> bool:
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO savings_goals (name, target_amount, saved_amount, deadline) "
                "VALUES (?, ?, 0, ?)",
                (name, target_amount, deadline),
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    def get_savings_goals(self) -> List[SavingsGoal]:
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id, name, target_amount, saved_amount, deadline "
            "FROM savings_goals ORDER BY id"
        )
        return [SavingsGoal(**dict(row)) for row in cursor.fetchall()]
    def add_to_savings(self, goal_id: int, amount: float) -> None:
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE savings_goals SET saved_amount = saved_amount + ? WHERE id = ?",
            (amount, goal_id),
        )
        self.conn.commit()
    def delete_savings_goal(self, goal_id: int) -> None:
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM savings_goals WHERE id = ?", (goal_id,))
        self.conn.commit()
    # ---------------- Aggregations ----------------
    def get_category_totals(self, year: int, month: int) -> List[Tuple[str, float]]:
        """Return (category, total) pairs for expenses in the given month."""
        cursor = self.conn.cursor()
        prefix = f"{year:04d}-{month:02d}"
        cursor.execute(
            "SELECT category, SUM(amount) AS total FROM transactions "
            "WHERE type = 'expense' AND date LIKE ? "
            "GROUP BY category ORDER BY total DESC",
            (prefix + "%",),
        )
        return [(row["category"], row["total"]) for row in cursor.fetchall()]
    def get_monthly_totals(self, months: int = 12) -> List[Tuple[str, float, float]]:
        """Return (month, expense_total, income_total) for the last N months."""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT substr(date, 1, 7) AS month, "
            "SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) AS expenses, "
            "SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) AS income "
            "FROM transactions GROUP BY month ORDER BY month"
        )
        rows = [(row["month"], row["expenses"], row["income"]) for row in cursor.fetchall()]
        return rows[-months:]
    def get_monthly_summary(self, year: int, month: int) -> Tuple[float, float, float]:
        """Return (income, expenses, balance) for the given month."""
        cursor = self.conn.cursor()
        prefix = f"{year:04d}-{month:02d}"
        cursor.execute(
            "SELECT "
            "COALESCE(SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END), 0) AS income, "
            "COALESCE(SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END), 0) AS expenses "
            "FROM transactions WHERE date LIKE ?",
            (prefix + "%",),
        )
        row = cursor.fetchone()
        income = row["income"]
        expenses = row["expenses"]
        return income, expenses, income - expenses
    def get_total_savings(self) -> float:
        cursor = self.conn.cursor()
        cursor.execute("SELECT COALESCE(SUM(saved_amount), 0) AS total FROM savings_goals")
        return cursor.fetchone()["total"]