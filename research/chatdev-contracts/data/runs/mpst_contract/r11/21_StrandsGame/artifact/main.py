"""Strands: word-segmentation puzzle entry point."""

from strands import PUZZLES

BANNER = "=== STRANDS: Word-Segmentation Puzzle ==="


def read_command(prompt):
    """Read a command; treat end-of-input (closed stdin) as a clean quit."""
    try:
        return input(prompt).strip().lower()
    except EOFError:
        print()
        return "quit"


def play(pz):
    """Run one puzzle to completion. Returns True if solved, False if skipped."""
    print(f"\n--- Puzzle: {pz.theme} ---")
    while not pz.is_complete():
        print("\n" + pz.display())
        cmd = read_command("Merge (e.g. '1 4') | hint | skip | quit > ")
        if cmd == "quit":
            print("Goodbye!")
            raise SystemExit
        if cmd == "skip":
            print("Puzzle skipped.")
            return False
        if cmd == "hint":
            print(pz.hint())
            continue
        _, msg = pz.merge(cmd.split())
        print(msg)
        if pz.is_complete():
            print(f"\nAll strands correctly merged -- '{pz.theme}' complete!")
    return True


def main():
    print(BANNER)
    print("Combine numbered strands to form hidden words or phrases.")
    solved = 0
    try:
        for pz in PUZZLES:
            if play(pz):
                solved += 1
    except KeyboardInterrupt:
        print("\nInterrupted -- goodbye!")
    print(f"\nFinished: {solved}/{len(PUZZLES)} puzzles solved. Thanks for playing!")


if __name__ == "__main__":
    main()