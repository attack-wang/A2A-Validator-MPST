'''Entry point for the two-player Pong game.
Run with:  python main.py
Requires:  pygame  (install with:  pip install pygame)
'''
import sys
def main():
    try:
        from game import Game
    except ImportError as error:
        raise SystemExit(
            "Could not start Pong: {}. "
            "Make sure pygame is installed (pip install pygame).".format(error)
        )
    Game().run()
if __name__ == "__main__":
    main()