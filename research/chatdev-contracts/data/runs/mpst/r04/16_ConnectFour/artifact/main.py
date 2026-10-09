'''
main.py
Entry point of the Connect Four application.
Creates the two players and the board, starts a Game, and offers
rematches until the players choose to quit.
'''
from board import Board
from player import Player
from game import Game
DEFAULT_NAMES = ("Player 1", "Player 2")
DISCS = ("X", "O")
def create_player(default_name, disc):
    """Ask for a player's name and return a Player with the given disc."""
    entered = input(f"Enter name for {default_name} (disc '{disc}'): ").strip()
    return Player(entered or default_name, disc)
def show_rules():
    """Print a short explanation of how to play."""
    print("\nHow to play:")
    print("  - The board has 7 columns and 6 rows.")
    print("  - Players take turns typing a column number (1-7).")
    print("  - The disc falls to the lowest empty row of that column.")
    print("  - First to line up 4 discs horizontally, vertically, or diagonally wins.")
    print("  - If the board fills up with no line of four, the game is a draw.")
def main():
    """Set up and run Connect Four sessions until the players quit."""
    print("Welcome to Connect Four!")
    show_rules()
    while True:
        board = Board()
        player1 = create_player(DEFAULT_NAMES[0], DISCS[0])
        player2 = create_player(DEFAULT_NAMES[1], DISCS[1])
        game = Game(player1, player2, board)
        game.play()
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != 'y':
            print("Thanks for playing Connect Four. Goodbye!")
            break
if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nGame interrupted. Goodbye!")