"""Reversi (Othello) command-line game."""

from game import Reversi, SIZE, EMPTY, BLACK, WHITE

SYMBOLS = {EMPTY: '.', BLACK: 'B', WHITE: 'W'}
COLS = 'abcdefgh'


def render(game):
    moves = set(game.valid_moves(game.current))
    lines = ['  ' + ' '.join(COLS)]
    for r in range(SIZE):
        cells = []
        for c in range(SIZE):
            if game.board[r][c] == EMPTY and (r, c) in moves:
                cells.append('*')
            else:
                cells.append(SYMBOLS[game.board[r][c]])
        lines.append(f'{r + 1} ' + ' '.join(cells))
    return '\n'.join(lines)


def parse(text):
    text = text.strip().lower()
    if len(text) == 2 and text[0] in COLS and text[1] in '12345678':
        return int(text[1]) - 1, COLS.index(text[0])
    return None


def main():
    game = Reversi()
    print('Reversi (Othello) - B=Black, W=White, *=valid move')
    print('Enter moves as column+row, e.g. d3. Type q to quit.')
    while not game.over():
        black, white = game.score()
        name = 'Black' if game.current == BLACK else 'White'
        print(f'\n{render(game)}')
        print(f'Score - Black: {black}  White: {white}')
        if not game.valid_moves(game.current):
            print(f'{name} has no valid move. Turn passes.')
            game.pass_turn()
            continue
        move = input(f'{name} to move (e.g. d3): ').strip().lower()
        if move in ('q', 'quit', 'exit'):
            print('Game aborted.')
            return
        pos = parse(move)
        if pos is None:
            print('Invalid input. Use a letter a-h and a number 1-8.')
            continue
        row, col = pos
        if game.play(row, col) is None:
            print('Invalid move there. Choose a square marked *.')
    print(f'\n{render(game)}')
    black, white = game.score()
    print(f'Final score - Black: {black}  White: {white}')
    if black > white:
        print('Black wins!')
    elif white > black:
        print('White wins!')
    else:
        print("It's a draw!")


if __name__ == '__main__':
    main()