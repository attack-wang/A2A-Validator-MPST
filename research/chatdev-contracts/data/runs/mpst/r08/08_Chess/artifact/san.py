'''
san.py
Parses player input in Standard Algebraic Notation (SAN) and matches it
against the list of legal moves. Handles castling (O-O / O-O-O), captures,
disambiguation, en passant annotations and promotion (e8=Q).
Returns (move, None) on success, (None, error_message) on failure, or
('PROMOTE', promo_moves) when a promotion piece must be chosen.
'''
import re
from pieces import Pawn, Knight, Bishop, Rook, Queen, King
SAN_PATTERN = re.compile(r'^([KQRBN])?([a-h])?([1-8])?x?([a-h][1-8])$')
def parse_san(board, color, raw, legal):
    text = raw.strip()
    if not text:
        return None, "Empty input. Enter a move in SAN (e.g. e4, Nf3, O-O)."
    text = text.replace('e.p.', '').replace('ep.', '').replace('e.p', '')
    text = re.sub(r'[+#!?]', '', text)
    text = text.strip()
    norm = text.replace('0', 'O')
    if norm in ('O-O', 'O-O-O'):
        rank = 7 if color == 'w' else 0
        target_file = 6 if norm == 'O-O' else 2
        for mv in legal:
            if (isinstance(mv.piece, King) and mv.from_sq == (4, rank)
                    and mv.to_sq == (target_file, rank)):
                return mv, None
        return None, f"Illegal move: {text} (castling not available)."
    promotion = None
    m = re.search(r'=\s*([QRBNqrbn])', text)
    if m:
        promotion = m.group(1).upper()
        text = (text[:m.start()] + text[m.end():]).strip()
    m = SAN_PATTERN.match(text)
    if not m:
        return None, (f"Could not parse '{raw}'. "
                      "Use SAN like e4, Nf3, exd5, O-O, e8=Q.")
    piece_letter, dfile, drank, dest = m.groups()
    tf = ord(dest[0]) - ord('a')
    tr = int(dest[1]) - 1
    cls = {'K': King, 'Q': Queen, 'R': Rook, 'B': Bishop, 'N': Knight}[piece_letter] if piece_letter else Pawn
    candidates = []
    for mv in legal:
        if mv.to_sq != (tf, tr):
            continue
        if not isinstance(mv.piece, cls):
            continue
        if dfile and mv.from_sq[0] != ord(dfile) - ord('a'):
            continue
        if drank and mv.from_sq[1] != int(drank) - 1:
            continue
        candidates.append(mv)
    if promotion:
        candidates = [mv for mv in candidates if mv.promotion == promotion]
        if not candidates:
            return None, f"Illegal move: {raw}"
        return candidates[0], None
    promo_moves = [mv for mv in candidates if mv.promotion is not None]
    if promo_moves and len(promo_moves) == len(candidates):
        return ('PROMOTE', promo_moves)
    if not candidates:
        return None, f"Illegal move: {raw}"
    if len(candidates) > 1:
        return None, (f"Ambiguous move: {raw}. "
                      "Add the departure file/rank, e.g. Nbd7 or R1e2.")
    return candidates[0], None