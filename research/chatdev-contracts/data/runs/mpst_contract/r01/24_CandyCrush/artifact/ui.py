"""Terminal interface for Candy Swap: rendering, input parsing, game loop."""
import os
from game import Match3Game, SYMBOLS, TARGET_SCORE

RESET = "\033[0m"
DELTAS = {"u": (-1, 0), "d": (1, 0), "l": (0, -1), "r": (0, 1)}


def render(game):
    print()
    print(f"Score: {game.score}/{TARGET_SCORE}   Moves left: {game.moves_left}")
    header = "   " + " ".join(str(c) for c in range(game.cols))
    print(header)
    for r in range(game.rows):
        row = " ".join(SYMBOLS[s][1] + s + RESET for s in game.board[r])
        print(f" {r} " + row)
    print(header)
    print("Candies: " + "  ".join(f"{code}={SYMBOLS[code][0]}" for code in SYMBOLS))


def parse_move(text):
    parts = text.lower().split()
    if len(parts) != 3 or len(parts[2]) != 1 or parts[2] not in DELTAS:
        return None
    if not (parts[0].isdigit() and parts[1].isdigit()):
        return None
    r, c = int(parts[0]), int(parts[1])
    dr, dc = DELTAS[parts[2]]
    return r, c, r + dr, c + dc


def find_hint(game):
    for r in range(game.rows):
        for c in range(game.cols):
            for dr, dc in ((0, 1), (1, 0)):
                if game.is_valid_move(r, c, r + dr, c + dc):
                    d = {(0, 1): "r", (1, 0): "d"}[(dr, dc)]
                    return f"{r} {c} {d}"
    return None


def prompt(text):
    try:
        return input(text)
    except (EOFError, KeyboardInterrupt):
        return "q"


def main():
    if os.name == "nt":
        os.system("")
    game = Match3Game()
    print("=== Candy Swap: a match-3 puzzle ===")
    print("Swap adjacent candies: type 'row col direction' (u/d/l/r), e.g. '2 3 r'")
    print(f"Reach {TARGET_SCORE} points within {game.moves_left} moves. Commands: h = hint, q = quit")
    while not game.over():
        render(game)
        text = prompt("Move (row col dir) > ").strip()
        if not text:
            continue
        cmd = text.lower()
        if cmd in ("q", "quit", "exit"):
            print(f"Thanks for playing! Final score: {game.score}")
            return
        if cmd in ("h", "hint"):
            hint = find_hint(game)
            print(f"Hint: try '{hint}'" if hint else "No moves available.")
            continue
        mv = parse_move(text)
        if mv is None:
            print("Invalid input. Use: row col direction (u/d/l/r).")
            continue
        if not (game.in_bounds(mv[0], mv[1]) and game.in_bounds(mv[2], mv[3])):
            print("Coordinates out of range.")
            continue
        result = game.move(*mv)
        if result is None:
            print("That swap forms no match - move rejected, try again.")
            continue
        points, cascades, shuffled = result
        msg = f"+{points} points"
        if cascades > 1:
            msg += f" (chain reaction x{cascades}!)"
        print(msg)
        if shuffled:
            print("No moves left on the board - candies reshuffled!")
    render(game)
    if game.score >= TARGET_SCORE:
        print(f"You win! Final score {game.score} with {game.moves_left} moves to spare.")
    else:
        print(f"Game over. Score {game.score}/{TARGET_SCORE}.")