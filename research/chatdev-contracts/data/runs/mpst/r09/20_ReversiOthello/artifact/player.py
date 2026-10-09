'''
player.py
Defines the Player class representing a participant in the Reversi
game, including prompting and validating the player's move input.
'''
from board import BLACK, WHITE, COLUMNS, parse_move
class Player:
    '''Represents a human Reversi player identified by disc color and name.'''
    SYMBOLS = {BLACK: 'X', WHITE: 'O'}
    def __init__(self, color, name=None):
        '''Create a player with the given disc color and optional name.'''
        self.color = color
        if name is None:
            name = 'Black player' if color == BLACK else 'White player'
        self.name = name
    @property
    def symbol(self):
        '''Single-character symbol used to render this player's discs.'''
        return self.SYMBOLS[self.color]
    def choose_move(self, valid_moves):
        '''Prompt until the player enters one of the given valid moves.
        Returns the chosen (row, col) tuple.'''
        while True:
            prompt = (f'{self.name} ({self.symbol}), enter your move '
                      f'[e.g. "d3" or "3 4"]: ')
            raw = input(prompt).strip()
            move = parse_move(raw)
            if move is None:
                print('  Invalid input. Use a column letter a-h plus row 1-8 '
                      '(e.g. "d3") or "row col" (e.g. "3 4").')
            elif move not in valid_moves:
                row, col = move
                print(f'  ({COLUMNS[col]}{row + 1}) is not a legal move. '
                      'Legal moves are marked with "*" on the board.')
            else:
                return move