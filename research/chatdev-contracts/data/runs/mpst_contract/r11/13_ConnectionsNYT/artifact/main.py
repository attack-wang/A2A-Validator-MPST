import os
from datetime import date
from game import Game
from puzzles import daily_puzzle

if os.name == "nt":
    os.system("")

RESET, BOLD, INV = "\033[0m", "\033[1m", "\033[7m"
COLORS = ["\033[93m", "\033[92m", "\033[94m", "\033[95m"]  # yellow green blue purple
WIDTH = 12


def cell(word, sel):
    return f"{INV if sel else ''}{word.center(WIDTH)}{RESET}"


def banner(text, color):
    return f"{color}{BOLD}{text.center(WIDTH * 4)}{RESET}"


def render(game):
    print()
    b = game.board
    for r in range(0, len(b), 4):
        print("".join(cell(w, w in game.selected) for w in b[r:r + 4]))
    dots = "● " * (game.max_mistakes - game.mistakes)
    print(f"\nMistakes remaining: {dots.strip() or 'none'}")
    for name, level, ws in game.solved:
        print(banner(f"{name}: {', '.join(ws)}", COLORS[level]))
    print("\nPick 4 (numbers or words), e.g. `1 5 9 13` | s=shuffle x=deselect q=quit")


def parse(game, line):
    toks = line.replace(",", " ").split()
    words, board = [], game.board
    for t in toks:
        if t.isdigit():
            i = int(t) - 1
            if not (0 <= i < len(board)):
                return None
            words.append(board[i])
        else:
            t = t.upper()
            if t not in board:
                return None
            words.append(t)
    return words


def main():
    game = Game(daily_puzzle())
    print(f"CHATDEV CONNECTIONS [{date.today().isoformat()}] - group the 16 words into 4 hidden sets of 4.")
    while not game.over:
        render(game)
        try:
            line = input("> ").strip().lower()
        except EOFError:
            print()
            return
        if line in ("q", "quit", "exit"):
            print("Bye.")
            return
        if line in ("s", "shuffle"):
            game.shuffle()
            continue
        if line in ("x", "deselect"):
            game.selected.clear()
            continue
        words = parse(game, line)
        if not words or len(set(words)) != 4:
            print("Choose exactly four distinct tiles.")
            continue
        game.selected = set(words)
        game.guess()
        kind, name = game.status
        left = game.max_mistakes - game.mistakes
        if kind == "correct":
            level, _ = next((l, ws) for n, l, ws in game.groups if n == name)
            print(banner(f"Correct! {name}", COLORS[level]))
        elif kind == "one_away":
            print(f"One away... keep going! ({left} mistakes remaining)")
        else:
            print(f"Nothing matches. ({left} mistakes remaining)")
    render(game)
    if game.won:
        print(banner("You solved today's puzzle!", COLORS[0]))
    else:
        print("Out of mistakes. The remaining groups:")
        done = {n for n, _, _ in game.solved}
        for name, level, ws in game.groups:
            if name not in done:
                print(banner(f"{name}: {', '.join(ws)}", COLORS[level]))


if __name__ == "__main__":
    main()