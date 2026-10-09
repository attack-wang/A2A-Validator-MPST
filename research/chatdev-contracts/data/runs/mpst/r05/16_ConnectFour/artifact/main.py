'''
main.py
Entry point for the Connect Four game.
Creates a Game instance (optionally with custom player names taken
from command-line arguments) and starts the match.
'''
import sys
from game import Game
def main():
    """Build the game with optional custom player names and start it."""
    names = sys.argv[1:3]
    player_one = names[0] if len(names) > 0 else "Player 1"
    player_two = names[1] if len(names) > 1 else "Player 2"
    game = Game(player_one, player_two)
    game.play()
if __name__ == "__main__":
    main()