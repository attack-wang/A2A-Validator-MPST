"""Console rendering and input for Gomoku."""

from board import EMPTY, BLACK, WHITE

SYMBOLS = {EMPTY: '.', BLACK: 'X', WHITE: 'O'}


class ConsoleUI:
    @staticmethod
    def welcome():
        print('=' * 48)
        print(' GOMOKU - five in a row on a 15x15 board')
        print(' Black (X) moves first. Enter moves as "row col".')
        print('=' * 48)

    @staticmethod
    def render(board):
        size = board.size
        print()
        print('    ' + ' '.join(f'{c:>2d}' for c in range(1, size + 1)))
        for r in range(size):
            cells = ' '.join(f'{SYMBOLS[v]:>2s}' for v in board.grid[r])
            print(f'{r + 1:>2d}  {cells}')
        print()

    @staticmethod
    def get_player_names():
        black = input('Name of Black player (X) [Black]: ').strip() or 'Black'
        white = input('Name of White player (O) [White]: ').strip() or 'White'
        return black, white

    @staticmethod
    def get_move(player, board):
        while True:
            try:
                raw = input(f'{player.name} ({SYMBOLS[player.stone]}), row col (1-{board.size}): ')
            except EOFError:
                raise SystemExit('\nInput closed. Game aborted.')
            parts = raw.replace(',', ' ').split()
            if len(parts) != 2:
                print('Invalid input. Enter two numbers, e.g. "8 8".')
                continue
            try:
                r, c = int(parts[0]), int(parts[1])
            except ValueError:
                print('Invalid input. Enter two integers.')
                continue
            if not board.is_empty(r - 1, c - 1):
                print('Cell is out of range or occupied. Try again.')
                continue
            return r - 1, c - 1

    @staticmethod
    def announce_win(player):
        print(f'*** {player.name} ({SYMBOLS[player.stone]}) wins with five in a row! ***')

    @staticmethod
    def announce_draw():
        print('*** The board is full. It is a draw! ***')

    @staticmethod
    def ask_replay():
        return input('Play again? (y/n): ').strip().lower() in ('y', 'yes')

    @staticmethod
    def farewell():
        print('Thanks for playing Gomoku. Goodbye!')