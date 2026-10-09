'''
Entry point for the Strands word-segmentation puzzle game.
This module parses command-line arguments (--gui/--console, --puzzle),
loads a built-in puzzle, constructs the StrandsGame engine, and launches
either the Tkinter GUI or the console UI. It replaces the previously
broken placeholder file that raised "NameError: name 'FILENAME' is not
defined" because the real entry-point code was never generated.
'''
import argparse
import sys
from puzzle_data import BUILT_IN_PUZZLES
from game_engine import StrandsGame
from console_ui import ConsoleUI
def parse_args(argv=None):
    """Parse command-line arguments for UI mode and puzzle selection."""
    parser = argparse.ArgumentParser(
        description=(
            "Strands: combine strands of text into meaningful words or "
            "phrases. Valid merges are confirmed; complete all targets "
            "to finish the puzzle."
        )
    )
    parser.add_argument(
        "--gui", action="store_true",
        help="launch the Tkinter GUI"
    )
    parser.add_argument(
        "--console", action="store_true",
        help="run in the console (default)"
    )
    parser.add_argument(
        "--puzzle", type=int, default=0,
        help="index of the built-in puzzle to play (default: 0)"
    )
    return parser.parse_args(argv)
def main(argv=None):
    """Select a puzzle, build the game engine, and start the requested UI."""
    args = parse_args(argv)
    if not BUILT_IN_PUZZLES:
        print("No puzzles available.")
        return 1
    # Clamp the puzzle index into the valid range so a bad --puzzle value
    # degrades gracefully instead of crashing.
    index = max(0, min(args.puzzle, len(BUILT_IN_PUZZLES) - 1))
    game = StrandsGame(BUILT_IN_PUZZLES[index])
    if args.gui:
        try:
            from gui import StrandsGUI
        except ImportError:
            # Tkinter missing on this platform: degrade to console mode
            # rather than crashing the whole application.
            print("Tkinter unavailable; falling back to console mode.")
            ConsoleUI(game).run()
        else:
            StrandsGUI(game).run()
    else:
        ConsoleUI(game).run()
    return 0
if __name__ == "__main__":
    sys.exit(main())