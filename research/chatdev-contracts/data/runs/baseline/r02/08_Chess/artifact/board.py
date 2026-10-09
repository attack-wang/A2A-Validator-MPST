'''
board.py
Board representation and core rules: piece placement, attack detection,
pseudo-legal/legal move generation, applying moves (including castling,
en passant and promotion) and position keys for repetition detection.
'''
from pieces import make_piece