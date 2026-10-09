'''
player.py
Defines the Player class for the Connect Four game.
A Player has a name and a disc symbol ('X' or 'O'). The get_move method
prompts the human user to type a column number, validates the choice
(it must be an integer within the board's column range and the column
must not already be full), and keeps re-prompting until a legal move is
entered. If the input stream is exhausted (EOFError, e.g. when running
non-interactively or after Ctrl+D/Ctrl+Z) or the session is interrupted
(KeyboardInterrupt), get_move returns None instead of crashing, so the
game can terminate gracefully.
'''
class Player:
    '''Represents one participant and handles their column input.'''
    def __init__(self, name, disc):
        '''Store the player's display name and disc symbol.'''
        self.name = name
        self.disc = disc
    def get_move(self, board):
        '''
        Prompt until the user supplies a valid 1-based column number for
        the given board. Returns the chosen column as an int, or None if
        the input stream is closed (EOFError) or the session is
        interrupted (KeyboardInterrupt).
        '''
        while True:
            try:
                raw = input(f'{self.name} ({self.disc}), choose a column '
                            f'(1-{board.cols}): ').strip()
            except EOFError:
                # stdin is closed or exhausted (non-interactive run,
                # Ctrl+D / Ctrl+Z): stop prompting instead of letting the
                # EOFError propagate and crash the program.
                print('\nNo more input available.')
                return None
            except KeyboardInterrupt:
                print('\nGame interrupted.')
                return None
            try:
                column = int(raw)
            except ValueError:
                print('Invalid input. Please type a column number.')
                continue
            if not board.is_valid_column(column):
                if 1 <= column <= board.cols:
                    print(f'Column {column} is already full. Pick another column.')
                else:
                    print(f'Column must be between 1 and {board.cols}.')
                continue
            return column