'''
main.py
This module is the entry point of the Reversi (Othello) game. It verifies
that the pygame dependency is installed, then creates the Game and GameUI
objects and starts the main application loop.
'''
import sys
def main():
    """Entry point: verify pygame is available, then launch the game UI."""
    try:
        import pygame  # noqa: F401  (availability check; ui.py imports pygame)
    except ImportError:
        print("pygame is required to run Reversi (Othello).")
        print("Install it with: pip install pygame")
        sys.exit(1)
    # Imported lazily so the friendly error message above is displayed
    # before ui.py (which imports pygame at module level) is loaded.
    from game import Game
    from ui import GameUI
    game = Game()
    ui = GameUI(game)
    ui.run()
if __name__ == "__main__":
    main()