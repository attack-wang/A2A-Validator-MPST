class Budget:
    def to_dict(self):
        return {
            "id": self.id,
            "category": self.category,
            "monthly_limit": self.monthly_limit,
        }
    @classmethod
    def from_dict(cls, data):
        return cls(
            category=data["category"],
            monthly_limit=data["monthly_limit"],
            budget_id=data.get("id"),
        )
    def __str__(self):
        return f"[{self.id[:8]}] {self.category}: ${self.monthly_limit:,.2f}/month"