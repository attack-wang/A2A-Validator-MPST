'''
main.py
Entry point for the Connect Four game. Collects the two player names
and starts the match. Every input() call is protected against closed
or interrupted input streams (EOFError / KeyboardInterrupt) so the
program always exits gracefully instead of crashing with a traceback.
'''
from game import Game
from player import Player
def get_player_name(default_name):
    """Ask for a player name, falling back to `default_name` if the
    input is empty, the stream is closed (EOF), or interrupted."""
    try:
        entered = input(
            f"{default_name}, enter your name "
            f"(press Enter to keep '{default_name}'): "
        ).strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return default_name
    return entered or default_name
def main():
    """Set up the players and run a full Connect Four match."""
    print("=" * 40)
    print("           CONNECT FOUR")
    print("=" * 40)
    try:
        player_one = Player(get_player_name("Player 1"), "X")
        player_two = Player(get_player_name("Player 2"), "O")
        game = Game(player_one, player_two)
        game.play()
    except (KeyboardInterrupt, EOFError):
        print("\nGame interrupted - goodbye!")
    else:
        print("Thanks for playing!")
if __name__ == "__main__":
    main()