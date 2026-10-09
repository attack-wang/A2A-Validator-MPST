'''
player.py
Defines the Player class, which stores a participant's name and disc
symbol and handles interactive, validated column selection.
'''
class Player:
    '''Represents a Connect Four player and collects their moves.'''
    def __init__(self, name: str, disc: str) -> None:
        '''Store the player's display name and disc symbol.'''
        self.name = name
        self.disc = disc
    def choose_column(self, board) -> int:
        '''Prompt until the player enters a valid, non-full column.
        The player types a 1-based column number; the matching 0-based
        index is returned so it can be used directly with the board.
        '''
        while True:
            prompt = f'{self.name} ({self.disc}), choose a column (1-{board.columns}): '
            raw = input(prompt).strip()
            if not raw:
                print('Please type a column number.')
                continue
            try:
                choice = int(raw)
            except ValueError:
                print(f'"{raw}" is not a number. Please enter a column number.')
                continue
            column = choice - 1
            if not board.is_valid_column(column):
                print(f'Column must be between 1 and {board.columns}. Try again.')
                continue
            if board.is_column_full(column):
                print(f'Column {choice} is already full. Choose another column.')
                continue
            return column