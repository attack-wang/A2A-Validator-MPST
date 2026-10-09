'''
main.py
Entry point for the Connect Four application.
Builds the board and the two players, starts the game loop, and wraps
the session with a friendly banner and graceful handling of interrupts
(KeyboardInterrupt / EOFError).
'''
from board import Board
from game import Game
from player import Player
def main():
    """Create the game objects and run one full Connect Four match."""
    print("=" * 42)
    print("           Welcome to Connect Four!")
    print("=" * 42)
    print("Drop discs into columns by typing a column number (1-7).")
    print("First to line up four discs horizontally, vertically,")
    print("or diagonally wins. Press Ctrl+C at any time to quit.")
    print()
    board = Board(rows=6, columns=7)
    player1 = Player("Player 1", "X")
    player2 = Player("Player 2", "O")
    game = Game(board=board, player1=player1, player2=player2)
    try:
        game.play()
    except (KeyboardInterrupt, EOFError):
        print("\nGame interrupted. Goodbye!")
        return
    print("Thanks for playing Connect Four!")
if __name__ == "__main__":
    main()