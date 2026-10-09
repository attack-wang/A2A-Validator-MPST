'''
main.py
Entry point of the two-player Pong game.
Creates the Game object and starts the main loop.
Run with: python main.py
Fix for the reported test failure (ModuleNotFoundError: No module named
'pygame'): the import of the game module is now guarded so that a missing
pygame installation produces a clear, actionable message instead of a raw
traceback. The dependency itself is declared in requirements.txt and can
be installed with: pip install -r requirements.txt
'''
import sys
def main():
    '''Create the game and run its main loop, reporting a missing pygame nicely.'''
    try:
        from game import Game
    except ImportError as error:
        missing = getattr(error, "name", "") or "required module"
        if "pygame" in missing or "pygame" in str(error):
            print("Could not start Pong: the 'pygame' module is not installed.")
            print("Install it with:  pip install pygame")
            print("Or install all dependencies with:  pip install -r requirements.txt")
        else:
            print("Could not start Pong: missing dependency '{}'.".format(missing))
            print("Install it with:  pip install {}".format(missing))
        sys.exit(1)
    Game().run()
if __name__ == "__main__":
    main()