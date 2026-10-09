'''
main.py
Entry point of the two-player Pong game. Creates the Game object and
starts the main loop. Run this file to play:  python main.py
'''
import sys
def main():
    try:
        import pygame  # noqa: F401  (imported to give a friendly error early)
        from game import Game
    except ImportError:
        print("The 'pygame' package is required to run this game.")
        print("Install it with:  pip install pygame")
        sys.exit(1)
    game = Game()
    game.run()
if __name__ == "__main__":
    main()