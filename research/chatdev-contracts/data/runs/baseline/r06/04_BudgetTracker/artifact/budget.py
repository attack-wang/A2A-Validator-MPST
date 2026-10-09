'''
budget.py
Data model for monthly budget settings: an overall monthly limit plus
optional per-category spending limits. Part of the budget tracker.
'''
class Budget:
    """Monthly budget: overall limit plus optional per-category limits."""
    def __init__(self, monthly_limit=0.0, category_limits=None):
        self.monthly_limit = self._validate_limit(monthly_limit)
        self.category_limits = {}
        for category, limit in (category_limits or {}).items():
            self.category_limits[str(category)] = self._validate_limit(limit)
    @staticmethod
    def _validate_limit(value):
        try:
            amount = float(value)
        except (TypeError, ValueError):
            raise ValueError("Budget limit must be a number")
        if amount < 0:
            raise ValueError("Budget limit cannot be negative")
        return round(amount, 2)
    def limit_for(self, category):
        """Per-category limit, or 0.0 when none is set."""
        return round(self.category_limits.get(category, 0.0), 2)
    def set_category_limit(self, category, limit):
        amount = self._validate_limit(limit)
        if amount <= 0:
            self.category_limits.pop(str(category), None)
        else:
            self.category_limits[str(category)] = amount
        return amount
    @property
    def has_limit(self):
        return self.monthly_limit > 0
    def to_dict(self):
        return {"monthly_limit": self.monthly_limit, "category_limits": dict(self.category_limits)}
    @classmethod
    def from_dict(cls, data):
        data = data or {}
        return cls(monthly_limit=data.get("monthly_limit", 0.0),
                   category_limits=data.get("category_limits", {}))
    def __repr__(self):
        return f"Budget(monthly={self.monthly_limit:.2f}, categories={len(self.category_limits)})"