'''
chess.py - A two-player terminal chess game.
Features:
- Full legal move generation (check filtering via simulation)
- Castling (O-O, O-O-O) with proper rights tracking
- En passant
- Pawn promotion (interactive prompt or =Q notation)
- SAN input parsing (disambiguation, captures, +/# suffixes)
- Check, checkmate, stalemate, insufficient material detection
- Commands: help, quit, resign, board, moves
Usage: python3 chess.py
'''
from dataclasses import dataclass
from typing import Optional, Tuple, List
WHITE = 'w'
BLACK = 'b'
KNIGHT_DELTAS = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
KING_DELTAS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
ORTHO = [(-1, 0), (1, 0), (0, -1), (0, 1)]
DIAG = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
@dataclass
class Move:
    origin: Tuple[int, int]
    destination: Tuple[int, int]
    piece: str
    captured: Optional[str] = None
    is_en_passant: bool = False
    castle: Optional[str] = None  # 'K' | 'Q' | None
    promotion: Optional[str] = None  # 'Q','R','B','N' or None
    is_double_push: bool = False