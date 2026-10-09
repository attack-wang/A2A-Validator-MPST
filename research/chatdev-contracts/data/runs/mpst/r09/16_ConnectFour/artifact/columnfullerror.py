class InvalidColumnError(ConnectFourError):
    """Raised when a chosen column index is outside the valid range."""
class ColumnFullError(ConnectFourError):
    """Raised when a chosen column has no empty cells remaining."""