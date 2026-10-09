class BudgetTracker:
    def __init__(self, storage):
        self.storage = storage
        self.transactions = []
        self.goals = []
        self.category_budgets = {}
        self.load()
    def load(self):
        state = self.storage.load()
        self.transactions = [Transaction.from_dict(d) for d in state["transactions"]]
        self.goals = [SavingsGoal.from_dict(d) for d in state["goals"]]
        self.category_budgets = {}
        for d in state["category_budgets"]:
            budget = CategoryBudget.from_dict(d)
            self.category_budgets[budget.name] = budget
    def save(self):
        state = {
            "transactions": [t.to_dict() for t in self.transactions],
            "goals": [g.to_dict() for g in self.goals],
            "category_budgets": [b.to_dict() for b in self.category_budgets.values()],
        }
        self.storage.save(state)