'''
main.py
Entry point for the Flappy Bird clone. Boots the Game object and starts
the main loop. If pygame is missing from the environment it exits with a
clear, actionable message instead of an opaque traceback.
'''
import sys
try:
    from game import Game
except ImportError as exc:
    if "pygame" in str(exc):
        print("The 'pygame' module is required but not installed.")
        print("Install it with:  pip install pygame")
        sys.exit(1)
    raise
def main():
    Game().run()
if __name__ == "__main__":
    main()