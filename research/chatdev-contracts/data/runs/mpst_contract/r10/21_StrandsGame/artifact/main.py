"""Strands - a word-segmentation puzzle played in the terminal."""

import sys

from strands import StrandsGame, PUZZLES

BANNER = """
=========================================
   S T R A N D S   ~   word merge puzzle
=========================================
Merge numbered strands to build every
hidden word or phrase. Valid merges are
confirmed and locked in, NYT-Strands style.
"""

HELP = ("Enter strand numbers separated by spaces (e.g. '1 4 7') to merge them.\n"
        "Commands: h = hint, r = reset, q = quit.")


def safe_input(prompt):
    """Read a line of input, returning None on EOF/interrupt instead of crashing."""
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        print()
        return None


def choose_puzzle():
    """Pick a puzzle via optional CLI argument, else an interactive menu."""
    arg = sys.argv[1] if len(sys.argv) > 1 else ""
    if arg.isdigit() and 1 <= int(arg) <= len(PUZZLES):
        return PUZZLES[int(arg) - 1]
    print("Available puzzles:")
    for i, p in enumerate(PUZZLES, 1):
        print(f"  {i}. {p['theme']} - {len(p['targets'])} answers, "
              f"{len(p['strands'])} strands")
    while True:
        choice = safe_input("Choose a puzzle: ")
        if choice is None:
            return None
        choice = choice.strip()
        if choice.isdigit() and 1 <= int(choice) <= len(PUZZLES):
            return PUZZLES[int(choice) - 1]
        print(f"Please enter a number between 1 and {len(PUZZLES)}.")


def main():
    print(BANNER)
    puzzle = choose_puzzle()
    if puzzle is None:
        print("\nNo puzzle selected - thanks for playing Strands!")
        return
    game = StrandsGame(**puzzle)
    print(f"\nTheme: {game.theme} - merge strands to form "
          f"{game.target_count} words/phrases.")
    print(HELP)
    while True:
        print("\n" + game.status())
        raw = safe_input("\nMerge > ")
        if raw is None:
            print("\nInput stream closed - thanks for playing Strands!")
            return
        cmd = raw.strip().lower()
        if cmd in ("q", "quit"):
            print("Thanks for playing Strands!")
            return
        if cmd in ("h", "hint"):
            print(game.hint())
            continue
        if cmd in ("r", "reset"):
            game.reset()
            print("Puzzle reset.")
            continue
        parts = cmd.replace(",", " ").split()
        if parts and all(p.isdigit() for p in parts):
            ok, feedback = game.try_merge([int(p) for p in parts])
            print(feedback)
            if ok and game.is_complete():
                print("\n" + game.status())
                print(f"\n*** ALL STRANDS MERGED! '{game.theme}' solved in "
                      f"{game.attempts} attempts. ***")
                return
        else:
            print(HELP)


if __name__ == "__main__":
    main()