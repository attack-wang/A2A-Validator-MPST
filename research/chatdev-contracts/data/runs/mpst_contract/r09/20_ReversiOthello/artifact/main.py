"""Reversi (Othello) console game. Run: python main.py"""

from reversi import Reversi, BLACK, WHITE, EMPTY

COLS = 'abcdefgh'


def render(game):
    moves = game.valid_moves()
    header = '  ' + ' '.join(COLS)
    lines = [header]
    for r in range(8):
        cells = []
        for c in range(8):
            value = game.board[r][c]
            cells.append('*' if value == EMPTY and (r, c) in moves else value)
        lines.append(f'{r + 1} ' + ' '.join(cells))
    lines.append(header)
    black, white = game.score()
    lines.append(f'Score -> X (Black): {black}   O (White): {white}')
    return '\n'.join(lines)


def parse_move(text):
    """Accept 'd3' or '3d' style input; return (row, col) or None."""
    text = text.strip().lower()
    if len(text) != 2:
        return None
    if text[0] in COLS and text[1].isdigit():
        col, row = COLS.index(text[0]), int(text[1]) - 1
    elif text[1] in COLS and text[0].isdigit():
        row, col = int(text[0]) - 1, COLS.index(text[1])
    else:
        return None
    return (row, col) if 0 <= row < 8 and 0 <= col < 8 else None


def read_line(prompt):
    """Read a line from stdin; return None on EOF or interrupt."""
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        return None


def main():
    game = Reversi()
    print('Reversi (Othello) - X (Black) moves first.')
    print('Enter moves as column+row, e.g. "d3". Type "quit" to exit.')
    while True:
        print()
        print(render(game))
        if game.game_over():
            black, white = game.score()
            if black > white:
                result = 'X (Black) wins!'
            elif white > black:
                result = 'O (White) wins!'
            else:
                result = "It's a draw!"
            print(f'Game over. Final score -> X: {black}  O: {white}. {result}')
            break
        if not game.valid_moves():
            print(f'{game.current} has no valid move; turn passes.')
            game.pass_turn()
            continue
        choice = read_line(f'{game.current}, your move (e.g. d3): ')
        if choice is None:
            print('\nInput stream closed; exiting. Thanks for playing!')
            break
        if choice.strip().lower() in ('quit', 'exit', 'q'):
            print('Thanks for playing!')
            break
        move = parse_move(choice)
        if move is None:
            print('Invalid input. Use a column letter and row number, e.g. d3.')
            continue
        if not game.apply_move(*move):
            print('Not a legal move. Choose a square marked "*".')


if __name__ == '__main__':
    main()