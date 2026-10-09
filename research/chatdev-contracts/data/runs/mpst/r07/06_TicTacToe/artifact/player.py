'''
player.py
Player module: represents a participant in the tic-tac-toe game,
holding their name, X/O symbol, and running win count across rounds.
'''
class Player:
    """A tic-tac-toe participant identified by a name and a symbol."""
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol
        self.wins = 0
    def add_win(self):
        """Increment this player's win counter after a victorious round."""
        self.wins += 1