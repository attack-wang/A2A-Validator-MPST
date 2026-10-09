'''
main.py
Entry point of the Connect Four application. It wires together the
board, the two players, the console interface, and the game logic,
then starts the match. The top-level guard handles both
KeyboardInterrupt and EOFError so a closed input stream or an
interrupt ends the program with a friendly message instead of a
traceback.
'''
from board import Board
from player import Player
from cli import CLI
from game import Game
def main():
    """Create the game components and start the Connect Four match."""
    board = Board(rows=6, cols=7)
    player1 = Player("Player 1", "X")
    player2 = Player("Player 2", "O")
    ui = CLI()
    ui.display_welcome()
    game = Game(board, player1, player2, ui)
    game.play()
if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        # EOFError is raised by input() when stdin is closed or
        # exhausted (e.g. redirected/empty input, Ctrl+D / Ctrl+Z).
        print("\nGame interrupted. Goodbye!")