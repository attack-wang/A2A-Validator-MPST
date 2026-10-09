@dataclass
class Move:
    """A legal move: a single step or a full multi-jump capture chain."""
    start: tuple          # (row, col) of the moving piece
    end: tuple            # (row, col) where the piece lands
    path: list            # ordered landing squares [(r, c), ...]
    captured: list        # ordered enemy squares removed [(r, c), ...]
    crowned: bool = False # True if the man is crowned on the landing square
    @property
    def is_capture(self):
        return bool(self.captured)