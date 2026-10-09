'''
Data models for the Budget Tracker application.
Defines the Expense and Saving dataclasses returned by the database layer.
'''
from dataclasses import dataclass
@dataclass
class Expense:
    """A single expense record."""
    id: int
    amount: float
    category: str
    description: str
    date: str
@dataclass
class Saving:
    """A single saving record."""
    id: int
    amount: float
    description: str
    date: str