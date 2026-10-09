'''
move.py
Defines the Move dataclass representing a single move on the board.
'''
from dataclasses import dataclass
from typing import Optional, Tuple
Position = Tuple[int, int]
@dataclass
class Move:
    """One move: from start to destination, optionally capturing a piece."""
    start: Position
    destination: Position
    captured: Optional[Position] = None  # position of captured piece, None for simple move
    @property
    def is_capture(self):
        """True if this move jumps over and removes an enemy piece."""
        return self.captured is not None