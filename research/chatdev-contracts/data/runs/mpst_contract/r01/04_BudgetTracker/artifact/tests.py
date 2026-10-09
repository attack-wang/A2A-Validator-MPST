import os
import tempfile
import unittest

from tracker import BudgetTracker


class BudgetTrackerTests(unittest.TestCase):
    def setUp(self):
        fd, self.path = tempfile.mkstemp(suffix=".json")
        os.close(fd)
        self.tracker = BudgetTracker(self.path)

    def tearDown(self):
        if os.path.exists(self.path):
            os.remove(self.path)

    def test_add_and_persist(self):
        self.tracker.add_transaction("income", "salary", 2000, "paycheck")
        self.tracker.add_transaction("expense", "food", 45.5, "groceries")
        fresh = BudgetTracker(self.path)
        self.assertEqual(len(fresh.list_transactions()), 2)

    def test_summary(self):
        self.tracker.add_transaction("income", "salary", 1000)
        self.tracker.add_transaction("expense", "rent", 400)
        self.tracker.add_transaction("savings", "bank", 100)
        s = self.tracker.summary()
        self.assertEqual(s["income"], 1000.0)
        self.assertEqual(s["expenses"], 400.0)
        self.assertEqual(s["savings"], 100.0)
        self.assertEqual(s["balance"], 600.0)

    def test_invalid_inputs(self):
        with self.assertRaises(ValueError):
            self.tracker.add_transaction("gift", "misc", 10)
        with self.assertRaises(ValueError):
            self.tracker.add_transaction("expense", "misc", -5)

    def test_remove(self):
        self.tracker.add_transaction("expense", "food", 10)
        removed = self.tracker.remove_transaction(0)
        self.assertEqual(removed["category"], "food")
        self.assertEqual(len(self.tracker.list_transactions()), 0)

    def test_category_breakdown(self):
        self.tracker.add_transaction("expense", "food", 30)
        self.tracker.add_transaction("expense", "food", 20)
        self.tracker.add_transaction("expense", "rent", 500)
        breakdown = self.tracker.category_breakdown()
        self.assertEqual(breakdown["rent"], 500.0)
        self.assertEqual(breakdown["food"], 50.0)


if __name__ == "__main__":
    unittest.main()