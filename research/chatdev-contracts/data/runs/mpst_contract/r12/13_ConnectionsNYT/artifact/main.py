"""ChatDev Connections - daily word-grouping puzzle. Run: python main.py"""
import random
import sys
from datetime import date

EPOCH = date(2024, 1, 1)
YELLOW, GREEN, BLUE, PURPLE = "\033[93m", "\033[92m", "\033[94m", "\033[95m"
RED, BOLD, RESET = "\033[91m", "\033[1m", "\033[0m"
DIFF_COLORS = [YELLOW, GREEN, BLUE, PURPLE]
DIFF_NAMES = ["straightforward", "medium", "hard", "tricky"]

PUZZLES = [
    [("KINDS OF BREAD", 0, ["RYE", "SOURDOUGH", "PUMPERNICKEL", "BAGUETTE"]),
     ("CARD GAMES", 1, ["HEARTS", "SPADES", "BRIDGE", "SOLITAIRE"]),
     ("___ BOARD", 2, ["KEY", "SKATE", "DART", "OUIJA"]),
     ("FISH", 3, ["BASS", "PIKE", "PERCH", "TROUT"])],
    [("SHADES OF BLUE", 0, ["NAVY", "TEAL", "COBALT", "AZURE"]),
     ("DOG BREEDS", 1, ["BEAGLE", "POODLE", "CORGI", "BOXER"]),
     ("MOVIE GENRES", 2, ["HORROR", "WESTERN", "ROMANCE", "THRILLER"]),
     ("THINGS WITH TEETH", 3, ["COMB", "SAW", "ZIPPER", "GEAR"])],
    [("UNITS OF MEASURE", 0, ["INCH", "LITER", "GRAM", "METER"]),
     ("CHESS PIECES", 1, ["ROOK", "BISHOP", "PAWN", "KNIGHT"]),
     ("STORMS", 2, ["BLIZZARD", "TYPHOON", "MONSOON", "SQUALL"]),
     ("CARD SUITS", 3, ["CLUB", "DIAMOND", "HEART", "SPADE"])],
    [("PLANETS", 0, ["MARS", "VENUS", "MERCURY", "SATURN"]),
     ("CANDY BARS", 1, ["TWIX", "SNICKERS", "CRUNCH", "PAYDAY"]),
     ("ROMAN DEITIES", 2, ["APOLLO", "DIANA", "MINERVA", "VULCAN"]),
     ("CAR MODELS", 3, ["MUSTANG", "CORVETTE", "CHARGER", "CAMARO"])],
    [("HOMOPHONES OF NUMBERS", 0, ["WON", "TOO", "FORE", "ATE"]),
     ("BOARD GAMES", 1, ["RISK", "CLUE", "SORRY", "SCRABBLE"]),
     ("COFFEE DRINKS", 2, ["LATTE", "MOCHA", "ESPRESSO", "AMERICANO"]),
     ("SHOE TYPES", 3, ["LOAFER", "SNEAKER", "CLOG", "STILETTO"])],
    [("PARTS OF A BOOK", 0, ["SPINE", "INDEX", "CHAPTER", "PREFACE"]),
     ("TENNIS TERMS", 1, ["ACE", "DEUCE", "LOB", "VOLLEY"]),
     ("PASTA SHAPES", 2, ["PENNE", "ORZO", "ZITI", "FUSILLI"]),
     ("___ LIGHT", 3, ["DAY", "SPOT", "FLASH", "MOON"])],
    [("DOG SOUNDS", 0, ["BARK", "WOOF", "HOWL", "GROWL"]),
     ("TREES", 1, ["MAPLE", "OAK", "CEDAR", "BIRCH"]),
     ("KNOCK ___", 2, ["WOOD", "UP", "DOWN", "OUT"]),
     ("CHEESES", 3, ["BRIE", "GOUDA", "FETA", "SWISS"])],
    [("GEMSTONES", 0, ["RUBY", "OPAL", "JADE", "TOPAZ"]),
     ("DANCE MOVES", 1, ["TWIST", "DIP", "SPIN", "SHIMMY"]),
     ("SONGBIRDS", 2, ["FINCH", "WREN", "LARK", "SPARROW"]),
     ("___ PRESS", 3, ["BENCH", "FRENCH", "PRINTING", "CIDER"])],
]


def daily_number():
    return (date.today() - EPOCH).days + 1


def print_board(board):
    print()
    for r in range(0, len(board), 4):
        print("   " + "".join(f"{r + c + 1:>2}. {board[r + c]:<13}" for c in range(4)))
    print()


def print_mistakes(used):
    marks = " ".join("●" if i < 4 - used else "✕" for i in range(4))
    print(f"Mistakes: {marks}  ({4 - used} left)")


def reveal(groups, solved):
    for gi, (name, diff, ws) in enumerate(groups):
        if gi not in solved:
            print(DIFF_COLORS[diff] + f"  {name} ({DIFF_NAMES[diff]}): {', '.join(ws)}" + RESET)


def main():
    day = daily_number()
    groups = PUZZLES[(day - 1) % len(PUZZLES)]
    owner = {w: gi for gi, (_, _, ws) in enumerate(groups) for w in ws}
    board = [w for _, _, ws in groups for w in ws]
    random.Random(day).shuffle(board)
    solved, mistakes = set(), 0
    print(f"\n{BOLD}CHATDEV CONNECTIONS{RESET} — Puzzle #{day} ({date.today().isoformat()})")
    print("Group the 16 words into 4 hidden categories of 4. Max 4 mistakes.")
    while True:
        print_board(board)
        print_mistakes(mistakes)
        raw = input("Pick four numbers (e.g. 1 5 9 13) | s=shuffle q=quit: ").strip().lower()
        if raw == "q":
            print("Bye!")
            return
        if raw == "s":
            random.shuffle(board)
            print("Shuffled.")
            continue
        toks = raw.replace(",", " ").split()
        try:
            picks = [int(t) - 1 for t in toks]
        except ValueError:
            print("Enter four numbers.")
            continue
        if len(picks) != 4 or len(set(picks)) != 4 or any(p < 0 or p >= len(board) for p in picks):
            print("Need four distinct numbers from the grid.")
            continue
        chosen = [board[p] for p in picks]
        owners = {owner[w] for w in chosen}
        if len(owners) == 1:
            gi = owners.pop()
            name, diff, ws = groups[gi]
            solved.add(gi)
            gone = set(ws)
            board = [w for w in board if w not in gone]
            print(DIFF_COLORS[diff] + f"\n✔ Correct — {name} ({DIFF_NAMES[diff]}): {', '.join(ws)}" + RESET)
            if not board:
                print(f"\n{GREEN}Perfect! You solved Puzzle #{day} with {mistakes} mistake(s).{RESET}")
                return
        else:
            best = max(sum(1 for w in chosen if owner[w] == o) for o in owners)
            mistakes += 1
            word = {1: "One", 2: "Two", 3: "Three"}[best]
            print(RED + f"✘ Incorrect — {word} away..." + RESET)
            if mistakes >= 4:
                print(f"\n{RED}Out of mistakes! Here is the solution:{RESET}")
                reveal(groups, solved)
                return


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nBye!")