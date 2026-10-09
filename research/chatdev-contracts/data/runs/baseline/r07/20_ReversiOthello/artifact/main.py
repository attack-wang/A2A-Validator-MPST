'''
main.py
Entry point of the Reversi (Othello) game. Creates the Game object and
starts the console game loop.
'''
from game import Game
def main():
    """Create and run a new Reversi game."""
    game = Game()
    try:
        game.play()
    except KeyboardInterrupt:
        print("\nGame interrupted. Goodbye!")
if __name__ == "__main__":
    main()