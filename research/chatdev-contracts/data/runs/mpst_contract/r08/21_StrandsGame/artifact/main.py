"""Strands - a word-segmentation puzzle. Run: python main.py"""
from strands import PUZZLES


def read_line(prompt):
    """Read input, guarding against EOF/interrupt so closed stdin exits cleanly."""
    try:
        return input(prompt)
    except EOFError:
        print("\n[input stream closed]")
        return "q"
    except KeyboardInterrupt:
        print("\n[interrupted]")
        return "q"


def show(p):
    print("\nTheme: %s" % p.theme)
    free = p.available()
    print("Strands: " + ", ".join("%d.'%s'" % (i + 1, p.strands[i].text) for i in free))
    print("Progress: %d/%d words found" % (len(p.found), len(p.answers)))


def main():
    print("=" * 52)
    print("Welcome to STRANDS - merge strands into real words!")
    print("Pick strand numbers that join into a word or phrase.")
    print("=" * 52)
    for num, p in enumerate(PUZZLES, 1):
        print("\n--- Puzzle %d of %d ---" % (num, len(PUZZLES)))
        while not p.is_complete():
            show(p)
            raw = read_line("Merge (e.g. 1 2 3) | h = hint | q = quit > ").strip().lower()
            if raw in ("q", "quit", "exit"):
                print("Thanks for playing Strands!")
                return
            if raw in ("h", "hint"):
                print(p.hint())
                continue
            try:
                idx = [int(t) - 1 for t in raw.replace(",", " ").split()]
            except ValueError:
                print("Enter strand numbers separated by spaces (e.g. 1 2 3).")
                continue
            _, msg = p.merge(idx)
            print(msg)
        print("\n*** '%s' solved! Words: %s ***" % (p.theme, ", ".join(p.found)))
    print("\nEvery strand merged. STRANDS complete - congratulations!")


if __name__ == "__main__":
    main()