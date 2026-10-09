@classmethod
def _transaction_from_dict(cls, record):
    if not isinstance(record, dict):
        raise ValueError("Transaction record must be a dict.")
    return Transaction(
        amount=record.get("amount", 0.0),
        category=record.get("category", "Uncategorized"),
        description=record.get("description", ""),
        t_type=record.get("t_type", TransactionType.EXPENSE),
        date=record.get("date", ""),
        transaction_id=record.get("transaction_id") or uuid.uuid4().hex,
    )