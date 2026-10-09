'''
main.py
Entry point: creates the Game and starts the main loop.
'''
try:
    from game import Game
except ImportError:
    print("The 'pygame' package is required to run this game.")
    print("Install it with:  pip install pygame")
    raise SystemExit(1)
if __name__ == "__main__":
    Game().run()