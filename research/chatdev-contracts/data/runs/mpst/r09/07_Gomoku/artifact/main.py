'''
main.py
Entry point for the Gomoku game.
Verifies that the required third-party dependency (pygame) is available
before starting the game and prints an actionable installation hint when
it is missing, instead of crashing with a raw traceback.
'''
import sys
def main():
    """Create and run the Gomoku game."""
    try:
        from game import Game
    except ModuleNotFoundError as error:
        if error.name == "pygame":
            sys.exit(
                "Missing dependency: the 'pygame' package is required to run "
                "Gomoku.\nInstall it with:\n    pip install pygame\n"
                "or:\n    pip install -r requirements.txt"
            )
        raise
    game = Game()
    game.run()
if __name__ == "__main__":
    main()