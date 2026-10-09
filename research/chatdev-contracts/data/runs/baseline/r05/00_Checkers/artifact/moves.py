'''
moves.py
Represents a legal move as an ordered path of squares plus the list of
captured (jumped) squares; multi-jumps produce multi-segment paths.
'''
from position import Position
class Move:
    def __init__(self, path, captures=None):
        self.path = list(path)
        self.captures = list(captures) if captures else []
    @property
    def is_capture(self):
        return bool(self.captures)
    @property
    def start(self):
        return self.path[0]
    @property
    def end(self):
        return self.path[-1]
    def notation(self):
        return "-".join(p.notation() for p in self.path)
    def __repr__(self):
        return f"Move({self.notation()})"