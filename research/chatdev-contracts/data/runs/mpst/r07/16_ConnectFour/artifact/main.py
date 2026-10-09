'''
main.py
Entry point for the Connect Four console application.
Builds the default game (a 6x7 board with two human players) and starts
the match. Run this file directly to play:  python main.py
A safety net around game.play() catches any residual EOFError or
KeyboardInterrupt (e.g. a closed stdin in non-interactive runs) so the
program always terminates with a clean, informative message instead of
a raw traceback.
'''
from game import Game
def main():
    '''Create and run a standard two-player Connect Four game.'''
    game = Game()
    try:
        game.play()
    except (EOFError, KeyboardInterrupt):
        # Defensive safety net: the input stream disappeared unexpectedly.
        print('\nGame terminated: input stream closed.')
if __name__ == '__main__':
    main()