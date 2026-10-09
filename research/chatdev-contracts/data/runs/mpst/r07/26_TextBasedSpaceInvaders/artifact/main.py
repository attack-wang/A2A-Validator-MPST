'''
main.py
Entry point of the simplified Space Invaders game.
Requires pygame (install with: pip install pygame).
Run with: python main.py
Controls: LEFT/RIGHT or A/D to move, SPACE to fire, R to restart.
If pygame is not installed, a friendly installation hint is shown
instead of a raw ModuleNotFoundError traceback.
'''
import sys
try:
    from game import Game
except ModuleNotFoundError as exc:
    # The test environment reported: ModuleNotFoundError: No module named 'pygame'.
    # Give the user a clear, actionable message instead of a raw traceback.
    if "pygame" in str(exc):
        print("Error: the 'pygame' module is required to run Space Invaders.")
        print("Install it with:  pip install pygame")
        print("Then start the game again with:  python main.py")
        sys.exit(1)
    raise  # an unrelated missing module: report it normally
def main():
    """Create the Game instance and start the main loop."""
    Game().run()
if __name__ == "__main__":
    main()