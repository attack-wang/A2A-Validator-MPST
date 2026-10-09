"""Strands - a word-segmentation puzzle. Run with: python main.py"""

import random

from strands import StrandsPuzzle

PUZZLES = [
    StrandsPuzzle(
        "Morning Menu",
        "Hint: things you might eat or drink at breakfast",
        [
            ("PANCAKE", ["PAN", "CAKE"]),
            ("OATMEAL", ["OAT", "MEAL"]),
            ("TOAST", ["TO", "AST"]),
            ("COFFEE", ["C", "OFF", "EE"]),
            ("MUFFIN", ["MUF", "FIN"]),
        ],
    ),
    StrandsPuzzle(
        "Sky & Sea",
        "Hint: compound words about nature",
        [
            ("RAINBOW", ["RAIN", "B", "OW"]),
            ("SNOWMAN", ["SNOW", "M", "AN"]),
            ("STARFISH", ["STAR", "F", "ISH"]),
            ("SUNBEAM", ["SUN", "BE", "AM"]),
            ("SEASHORE", ["SEA", "SH", "ORE"]),
        ],
    ),
    StrandsPuzzle(
        "Home Sweet Home",
        "Hint: furniture and fittings around the house",
        [
            ("LAMP", ["LA", "MP"]),
            ("CHAIR", ["CH", "AIR"]),
            ("TABLE", ["TAB", "LE"]),
            ("WINDOW", ["WIN", "DOW"]),
            ("MIRROR", ["MIR", "ROR"]),
        ],
    ),
]


def show_board(puzzle):
    print("\n" + "=" * 46)
    print(f"PUZZLE: {puzzle.name}   (found {len(puzzle.found)}/{len(puzzle.entries)})")
    print(puzzle.theme)
    print("=" * 46)
    pool = puzzle.pool
    for row in range(0, len(pool), 4):
        print("   ".join(f"{s.sid:>2}:{s.text:<6}" for s in pool[row:row + 4]))
    if puzzle.found:
        print("Found: " + ", ".join(puzzle.found))


def parse_ids(raw):
    raw = raw.replace("+", " ").replace(",", " ")
    return [int(token) for token in raw.split()]


def read_line(prompt):
    """Read a line of input; return None when the input stream is closed."""
    try:
        return input(prompt)
    except EOFError:
        return None


def play(puzzle):
    print(f"\nNew board: {puzzle.name} - merge the strands into "
          f"{len(puzzle.entries)} words!")
    while True:
        if puzzle.is_complete():
            print("\n*** All strands correctly merged - puzzle complete! ***")
            return
        show_board(puzzle)
        raw = read_line("\nMerge strands by number (e.g. '1 3'), "
                        "or 'hint'/'shuffle'/'quit': ")
        if raw is None:
            print("\nInput stream closed - thanks for playing Strands!")
            raise SystemExit
        raw = raw.strip().lower()
        if raw == "quit":
            print("Thanks for playing Strands!")
            raise SystemExit
        if raw == "shuffle":
            puzzle.reset()
            print("Board shuffled (found words kept).")
            continue
        if raw == "hint":
            unfound = [d for d, _, _ in puzzle.entries if d not in puzzle.found]
            word = random.choice(unfound)
            print(f"Hint: an unfound word starts with '{word[:2]}...' "
                  f"({len(word)} letters total).")
            continue
        try:
            sids = parse_ids(raw)
        except ValueError:
            print("Enter strand numbers separated by spaces, e.g. '1 3'.")
            continue
        if not sids:
            continue
        _, message = puzzle.merge(sids)
        print(">>> " + message)


def main():
    print("Welcome to STRANDS - the word-segmentation puzzle!")
    print("Combine numbered strands to form meaningful words; "
          "find them all to win.")
    solved = 0
    try:
        for puzzle in PUZZLES:
            play(puzzle)
            solved += 1
    except KeyboardInterrupt:
        print()
    if solved == len(PUZZLES):
        print("\nYou conquered every board. Brilliant strand work!")


if __name__ == "__main__":
    main()