'''
main.py
Entry point for the Connect Four game.
Running this file starts an interactive, two-player, console-based
Connect Four match:
  * Two players alternate typing a column number (1-7).
  * The disc falls to the lowest empty cell of the chosen column.
  * The board is re-rendered after every move.
  * The game ends when a player forms a horizontal, vertical, or
    diagonal line of four discs, or when the grid is full (draw).
  * Column choices are validated; invalid input is re-prompted.
  * Interrupts (Ctrl+C) reaching the top level exit cleanly without
    a raw traceback.
'''
from game import Game
def main():
    """Create a Game instance and run the match loop."""
    game = Game()
    try:
        game.run()
    except KeyboardInterrupt:
        # Last-resort guard: any interrupt outside the guarded input
        # helpers still exits cleanly instead of a raw traceback.
        print("\nInterrupted. Thanks for playing Connect Four. Goodbye!")
        raise SystemExit(0)
if __name__ == "__main__":
    main()