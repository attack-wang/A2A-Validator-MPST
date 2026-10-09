import uuid
class Transaction:
    def __init__(self, date, description, amount, category, ttype, transaction_id=None):
        self.id = transaction_id if transaction_id else str(uuid.uuid4())
        ...