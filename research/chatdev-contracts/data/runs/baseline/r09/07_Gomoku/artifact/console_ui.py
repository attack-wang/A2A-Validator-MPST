'''
console_ui.py
Provides a terminal-based user interface for the Gomoku game,
including board rendering, move input parsing, and status messages.
'''
import re
import string
from game import Game
from constants import BOARD_SIZE, BLACK, WHITE
class ConsoleUI:
    '''Terminal interface for playing Gomoku.'''
    COLUMN_LABELS = string.ascii_uppercase[:BOARD_SIZE]  # 'A'..'O'
    def __init__(self, game=None):
        self.game = game if game is not None else Game()
    def run(self):
        self.print_welcome()
        while True:
            self.play_match()
            if not self.ask_play_again():
                break
            self.game.reset()
        print('Thanks for playing Gomoku. Goodbye!')
    def play_match(self):
        while not self.game.game_over:
            self.render_board()
            player = self.game.current_player
            prompt = f"{player.name} ({player.symbol}), your move (e.g. 'H8' or '8 8'): "
            move = self.get_move(prompt)
            if move is None:
                continue  # invalid input message already shown
            row, col = move
            if not self.game.play_turn(row, col):
                print('That intersection is occupied or out of range. Try again.')
        self.render_board()
        self.announce_result()
    def print_welcome(self):
        '''Explain the board layout and accepted input formats.'''
        print('=' * 46)
        print('Welcome to Gomoku (Five in a Row)!')
        print(f'Board: {BOARD_SIZE}x{BOARD_SIZE}. Black (●) moves first.')
        print("Enter moves as 'H8' (column+row) or '8 8' (row col), 1-15. 'q' quits.")
        print('=' * 46)
    def render_board(self):
        '''Print the current board with column letters and row numbers.'''
        print('   ' + ' '.join(self.COLUMN_LABELS))
        for r in range(BOARD_SIZE):
            cells = []
            for c in range(BOARD_SIZE):
                cell = self.game.board.get_cell(r, c)
                cells.append('●' if cell == BLACK else '○' if cell == WHITE else '·')
            print(f'{r + 1:2d} ' + ' '.join(cells))
    def parse_move(self, text):
        '''Parse "H8", "8H", "8 8" or "8,8" into 0-indexed (row, col); None if invalid.'''
        text = text.strip().upper().replace(',', ' ')
        compact = text.replace(' ', '')
        m = re.fullmatch(r'([A-O])(\d{1,2})', compact)
        if m:
            row, col = int(m.group(2)) - 1, ord(m.group(1)) - ord('A')
        else:
            m = re.fullmatch(r'(\d{1,2})([A-O])', compact)
            if m:
                row, col = int(m.group(1)) - 1, ord(m.group(2)) - ord('A')
            else:
                tokens = text.split()
                if len(tokens) == 2 and all(t.isdigit() for t in tokens):
                    row, col = int(tokens[0]) - 1, int(tokens[1]) - 1
                else:
                    return None
        return (row, col) if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE else None
    def get_move(self, prompt):
        '''Prompt for one move; returns (row, col) or None for invalid input.'''
        try:
            text = input(prompt)
        except (EOFError, KeyboardInterrupt):
            print()
            raise SystemExit(0)
        if text.strip().lower() in ('q', 'quit', 'exit'):
            raise SystemExit(0)
        move = self.parse_move(text)
        if move is None:
            print("Invalid input. Use 'H8' style or '8 8' (row col), 1-15.")
        return move
    def announce_result(self):
        '''Print the final outcome of the match.'''
        if self.game.winner_color is not None:
            winner = self.game.players[self.game.winner_color]
            print(f'{winner.name} ({winner.symbol}) wins with five in a row!')
        else:
            print('Board is full - it is a draw!')
    def ask_play_again(self):
        '''Ask whether the user wants another match.'''
        try:
            answer = input('Play again? (y/n): ')
        except (EOFError, KeyboardInterrupt):
            print()
            return False
        return answer.strip().lower().startswith('y')