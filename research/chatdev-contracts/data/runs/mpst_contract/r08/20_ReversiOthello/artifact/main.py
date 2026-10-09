"""Reversi (Othello) — two-player command-line game. Run: python main.py"""

from game import Reversi, SIZE, EMPTY, BLACK, WHITE

NAMES = {BLACK: 'Black', WHITE: 'White'}


def parse_move(text):
    """Parse 'd3', '3d', 'd 3' or '3 5' into (row, col); None if invalid."""
    text = text.strip().lower().replace(',', ' ')
    parts = text.split()
    if len(parts) == 1 and len(parts[0]) == 2:
        parts = list(parts[0])
    if len(parts) != 2:
        return None
    a, b = parts
    if a.isalpha() and b.isdigit():
        row, col = int(b) - 1, ord(a) - ord('a')
    elif a.isdigit() and b.isalpha():
        row, col = int(a) - 1, ord(b) - ord('a')
    elif a.isdigit() and b.isdigit():
        row, col = int(a) - 1, int(b) - 1
    else:
        return None
    return (row, col) if Reversi.in_bounds(row, col) else None


def render(game):
    """Board with '*' on valid moves for the player to act, plus the score."""
    moves = set(game.valid_moves(game.current))
    lines = ['  ' + ' '.join(chr(ord('a') + c) for c in range(SIZE))]
    for r in range(SIZE):
        cells = [game.board[r][c] if game.board[r][c] != EMPTY or (r, c) not in moves
                 else '*' for c in range(SIZE)]
        lines.append(f'{r + 1} ' + ' '.join(cells))
    black, white = game.score()
    lines.append(f'Score - Black: {black}  White: {white}')
    return '\n'.join(lines)


def announce_result(game):
    black, white = game.score()
    if black > white:
        result = 'Black wins!'
    elif white > black:
        result = 'White wins!'
    else:
        result = 'Draw.'
    print(f'Game over - final score: Black {black}, White {white}. {result}')


def main():
    game = Reversi()
    print('Reversi (Othello): two players take turns. Enter moves as column+row, e.g. d3.')
    print('Valid moves are marked with "*". Type q to quit.')
    while not game.is_over():
        if not game.valid_moves(game.current):
            print(f'\n{NAMES[game.current]} has no valid moves - turn passes.')
            game.pass_turn()
            continue
        print()
        print(render(game))
        print(f"{NAMES[game.current]} to move.")
        while True:
            try:
                text = input('> ').strip()
            except (EOFError, KeyboardInterrupt):
                print('\nInput stream closed - game aborted.')
                return
            if text.lower() in ('q', 'quit', 'exit'):
                print('Game aborted.')
                return
            move = parse_move(text)
            if move and game.apply_move(move[0], move[1], game.current):
                break
            print('Invalid move - choose a cell marked "*".')
    print()
    print(render(game))
    announce_result(game)


if __name__ == '__main__':
    main()