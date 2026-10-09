#!/usr/bin/env python3
"""Checkers (Draughts): two-player console game with standard rules."""

MAN_DIRS = {'r': ((-1, -1), (-1, 1)), 'b': ((1, -1), (1, 1))}
ALL_DIRS = ((-1, -1), (-1, 1), (1, -1), (1, 1))
FILES = 'abcdefgh'


class Checkers:
    def __init__(self):
        self.board = [[None] * 8 for _ in range(8)]
        for r in range(8):
            for c in range(8):
                if (r + c) % 2:
                    if r < 3:
                        self.board[r][c] = 'b'
                    elif r > 4:
                        self.board[r][c] = 'r'
        self.turn = 'r'

    @staticmethod
    def inside(r, c):
        return 0 <= r < 8 and 0 <= c < 8

    @staticmethod
    def dirs(piece):
        return ALL_DIRS if piece.isupper() else MAN_DIRS[piece]

    def _captures(self, r, c, board, piece, seq):
        out = []
        enemy = 'b' if piece.lower() == 'r' else 'r'
        for dr, dc in self.dirs(piece):
            mr, mc, lr, lc = r + dr, c + dc, r + 2 * dr, c + 2 * dc
            if (self.inside(lr, lc) and board[mr][mc]
                    and board[mr][mc].lower() == enemy and board[lr][lc] is None):
                nb = [row[:] for row in board]
                nb[r][c] = nb[mr][mc] = None
                np_ = piece
                crowned = piece.islower() and lr == (0 if piece == 'r' else 7)
                if crowned:
                    np_ = piece.upper()
                nb[lr][lc] = np_
                if crowned:
                    out.append(seq + [(lr, lc)])
                else:
                    deeper = self._captures(lr, lc, nb, np_, seq + [(lr, lc)])
                    out.extend(deeper if deeper else [seq + [(lr, lc)]])
        return out

    def piece_moves(self, r, c):
        piece = self.board[r][c]
        caps = self._captures(r, c, self.board, piece, [])
        if caps:
            return caps, True
        quiet = []
        for dr, dc in self.dirs(piece):
            lr, lc = r + dr, c + dc
            if self.inside(lr, lc) and self.board[lr][lc] is None:
                quiet.append([(r, c), (lr, lc)])
        return quiet, False

    def legal_moves(self, player):
        caps, quiet = [], []
        for r in range(8):
            for c in range(8):
                if self.board[r][c] and self.board[r][c].lower() == player:
                    mv, is_cap = self.piece_moves(r, c)
                    (caps if is_cap else quiet).extend(mv)
        return caps, quiet

    def parse(self, text):
        s = ''.join(text.lower().split()).replace('-', '').replace('>', '')
        if not s or len(s) % 2:
            return None
        seq = []
        for i in range(0, len(s), 2):
            f, rk = s[i], s[i + 1]
            if f not in FILES or rk not in '12345678':
                return None
            seq.append((int(rk) - 1, ord(f) - 97))
        return seq

    def apply(self, seq):
        caps, quiet = self.legal_moves(self.turn)
        if seq not in (caps if caps else quiet):
            return False
        (r, c), rest = seq[0], seq[1:]
        piece = self.board[r][c]
        self.board[r][c] = None
        for lr, lc in rest:
            if abs(lr - r) == 2:
                self.board[(lr + r) // 2][(lc + c) // 2] = None
            r, c = lr, lc
        if piece.islower() and r == (0 if piece == 'r' else 7):
            piece = piece.upper()
        self.board[r][c] = piece
        self.turn = 'b' if self.turn == 'r' else 'r'
        return True

    def render(self):
        lines = ['   a b c d e f g h']
        for r in range(8):
            cells = []
            for c in range(8):
                p = self.board[r][c]
                cells.append(p if p else ('.' if (r + c) % 2 else ' '))
            lines.append(f'{r + 1}  ' + ' '.join(cells))
        return '\n'.join(lines)


def main():
    game = Checkers()
    names = {'r': 'Red', 'b': 'Black'}
    print('Checkers (Draughts)')
    print('Red starts on rows 6-8 and moves up; Black starts on rows 1-3 and moves down.')
    print('Moves: from-to squares, e.g. c3-d4; multi-jumps: c3-e5-g7. Captures are mandatory.')
    print("Type 'quit' to exit.")
    while True:
        print('\n' + game.render())
        caps, quiet = game.legal_moves(game.turn)
        if not caps and not quiet:
            print(f"{names['b' if game.turn == 'r' else 'r']} wins!")
            break
        if caps:
            print('Capture is mandatory.')
        try:
            text = input(f"{names[game.turn]}'s move: ").strip()
        except (EOFError, KeyboardInterrupt):
            print('\nGame ended.')
            break
        if text.lower() in ('quit', 'exit', 'q'):
            print('Game ended.')
            break
        if not game.apply(game.parse(text) or []):
            print('Invalid move, try again.')


if __name__ == '__main__':
    main()