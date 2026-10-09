class Game:
    def __init__(self):
        self.board = Board()
        self.turn = 'w'
        self.castling_rights = {'K': True, 'Q': True, 'k': True, 'q': True}
        self.en_passant_target = None
        self.halfmove_clock = 0
        self.fullmove_number = 1
        self.move_history = []      # list of SAN strings
        self.position_counts = {}   # repetition detection
        self._record_position()
    # ---- position key for repetition ----
    def _position_key(self):
        rows = []
        for r in range(8):
            row = []
            for c in range(8):
                p = self.board.grid[r][c]
                row.append(p.ascii_symbol() if p else '.')
            rows.append(''.join(row))
        ep = square_name(self.en_passant_target) if self.en_passant_target else '-'
        rights = ''.join(k for k in ('KQkq') if self.castling_rights.get(k)) or '-'
        return ' '.join(rows) + ' ' + self.turn + ' ' + rights + ' ' + ep
    def _record_position(self):
        key = self._position_key()
        self.position_counts[key] = self.position_counts.get(key, 0) + 1