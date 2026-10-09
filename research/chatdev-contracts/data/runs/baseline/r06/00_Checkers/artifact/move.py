class Move:
    def __init__(self, path, captures=None):
        self.path = list(path)
        self.captures = list(captures or [])
    @property
    def start(self): return self.path[0]
    @property
    def end(self): return self.path[-1]
    @property
    def is_capture(self): return bool(self.captures)
    def notation(self):
        sep = 'x' if self.is_capture else '-'
        return sep.join(format_position(r, c) for r, c in self.path)
    def __eq__(self, other):
        if not isinstance(other, Move): return NotImplemented
        return self.path == other.path and self.captures == other.captures
    def __hash__(self):
        return hash((tuple(self.path), tuple(self.captures)))
    def __repr__(self):
        return f"Move({self.notation()!r}, captures={...})"