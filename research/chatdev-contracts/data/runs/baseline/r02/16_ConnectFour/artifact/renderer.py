'''
renderer.py
This module defines the Renderer class, responsible for displaying the
Connect Four board and game messages in the console.
'''
class Renderer:
    """Handles console rendering of the Connect Four board and messages."""
    def render_board(self, board):
        """Print the board grid with 1-indexed column numbers above and below."""
        header = ' ' + ' '.join(str(col + 1) for col in range(board.cols))
        separator = ' ' + '-' * (2 * board.cols + 1)
        print()
        print(header)
        print(separator)
        for row in board.grid:
            print('|' + '|'.join(row) + '|')
        print(separator)
        print(header)
        print()
    def show_message(self, message):
        """Print a game message to the console."""
        print(message)
    def show_turn(self, player, cols):
        """Announce whose turn it is, using the board's column count
        so the prompt stays correct for any grid size."""
        print(f"{player.name}'s turn ({player.disc}). Choose a column (1-{cols}):")