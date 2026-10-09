# ui.py
'''Console user interface for the Reversi (Othello) game.'''
from board import EMPTY, BLACK, WHITE
class ConsoleUI:
    '''Handles all console input and output for the game.'''
    def display_message(self, message):
        '''Print a message to the console.'''
        print(message)
    def display_board(self, board, valid_moves=None):
        '''Print the current board, optionally marking valid moves with "*".'''
        print()
        print(board.display(valid_moves))
    def display_score(self, board, players):
        '''Print the current score for both players.'''
        scores = [(p.name, board.count_discs(p.disc)) for p in players]
        print('Score: ' + ' | '.join(f'{name} ({p.disc}): {s}' ...))