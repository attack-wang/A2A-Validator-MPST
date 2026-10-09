'''
player.py
Defines the Player class for the Gomoku game: a named participant with a
stone color, plus console input handling that keeps prompting until the
player provides a legal move or chooses to quit. The input() call is
guarded so that EOF (closed/exhausted stdin) or Ctrl+C is treated as a
graceful quit signal instead of crashing with an unhandled traceback.
'''
class Player:
    '''Represents a Gomoku player and how they enter their moves.'''
    def __init__(self, name, stone):
        '''Store the player's display name and stone color code.'''
        self.name = name
        self.stone = stone
    def get_move(self, board):
        '''Prompt until a valid (row, col) is entered; None means quit.
        Accepts input like "7 8" or "7,8". Re-prompts on malformed input,
        out-of-bounds coordinates, or occupied cells. EOFError and
        KeyboardInterrupt are caught and mapped to the established quit
        path (returning None), so the game shuts down cleanly even when
        stdin is closed or the user interrupts the program.
        '''
        while True:
            try:
                raw = input(
                    f'{self.name}, enter your move (row col) or q to quit: '
                ).strip().lower()
            except (EOFError, KeyboardInterrupt):
                print()  # keep output tidy after the interrupted prompt
                return None  # reuse the established quit path
            if raw in ('q', 'quit', 'exit'):
                return None
            tokens = raw.replace(',', ' ').split()
            if len(tokens) != 2:
                print('Invalid input. Please enter two numbers, e.g. "7 8".')
                continue
            try:
                row, col = int(tokens[0]), int(tokens[1])
            except ValueError:
                print('Invalid input. Row and column must be integers.')
                continue
            if board.is_valid_move(row, col):
                return row, col
            print('That cell is out of bounds or already occupied. Try again.')