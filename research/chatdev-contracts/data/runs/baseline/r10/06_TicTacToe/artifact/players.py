'''
players.py
Player definitions for the Tic-Tac-Toe application.
The Player class models one participant of the game, identified by a
board symbol ("X" or "O") and a human-readable display name shown in
the interface and status messages.
'''
class Player:
    '''Represents a single Tic-Tac-Toe player and their mark.'''
    VALID_SYMBOLS = ("X", "O")
    def __init__(self, symbol, name=None):
        '''
        Create a player.
        :param symbol: The mark placed on the board, "X" or "O".
        :param name:   Optional display name; defaults to "Player X"/"Player O".
        '''
        if symbol not in self.VALID_SYMBOLS:
            raise ValueError("Player symbol must be 'X' or 'O', got '{}'.".format(symbol))
        self._symbol = symbol
        self._name = name if name else "Player {}".format(symbol)
    def get_symbol(self):
        '''Return the board symbol used by this player.'''
        return self._symbol
    def get_name(self):
        '''Return the display name of this player.'''
        return self._name
    def __str__(self):
        '''Human-readable representation, e.g. "Player X (X)".'''
        return "{} ({})".format(self._name, self._symbol)