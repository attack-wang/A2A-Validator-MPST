    def load_transactions(self):
        """Load all transactions, skipping any malformed records."""
        transactions = []
        for item in self._load_list(self.transactions_path):
            try:
                transactions.append(Transaction.from_dict(item))
            except (ValueError, TypeError, KeyError, AttributeError):
                continue
        return transactions