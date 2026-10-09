"""Console display and input handling for Reversi (Othello)."""

from board import Board

SYMBOLS = {Board.EMPTY: '.', Board.BLACK: 'X', Board.WHITE: 'O'}


def render(board, moves):
    lines = ['  ' + ' '.join(chr(ord('a') + c) for c in range(Board.SIZE))]
    for r in range(Board.SIZE):
        row = []
        for c in range(Board.SIZE):
            row.append('*' if (r, c) in moves else SYMBOLS[board.grid[r][c]])
        lines.append(f'{r + 1} ' + ' '.join(row))
    return '\n'.join(lines)


def show_status(game):
    """Print board, score, and current player's valid moves; return the move dict."""
    moves = game.board.valid_moves(game.current)
    black, white = game.board.score()
    print(render(game.board, moves))
    print(f'Score - Black (X): {black}  White (O): {white}')
    name = 'Black (X)' if game.current == Board.BLACK else 'White (O)'
    hints = ', '.join(f'{r + 1}{chr(ord("a") + c)}' for r, c in sorted(moves))
    print(f'{name} to move. Valid moves: {hints or "none"}')
    return moves


def read_move(moves):
    """Prompt until a valid move is entered; returns (r, c) or None to quit."""
    while True:
        try:
            raw = input('Enter move (e.g. 3d) or q to quit: ').strip().lower()
        except (EOFError, KeyboardInterrupt):
            return None
        if raw == 'q':
            return None
        if len(raw) == 2 and raw[0].isdigit() and raw[1].isalpha():
            r, c = int(raw[0]) - 1, ord(raw[1]) - ord('a')
            if (r, c) in moves:
                return r, c
        print('Invalid move. Try again.')