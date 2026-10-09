from game import Game

DIRS = {"u": (-1, 0), "d": (1, 0), "l": (0, -1), "r": (0, 1)}


def draw(game):
    b, n = game.board, game.board.size
    print("\n    " + " ".join(str(c) for c in range(n)))
    for r in range(n):
        print(f"{r:2d}  " + " ".join(b.cell(t) for t in b.grid[r]))
    print(f"\nScore {game.score}/{game.TARGET}   Moves left {game.moves_left}")


def parse(raw):
    t = raw.split()
    if len(t) == 3 and t[2] in DIRS:
        r, c = int(t[0]), int(t[1])
        dr, dc = DIRS[t[2]]
        return (r, c), (r + dr, c + dc)
    if len(t) == 4:
        return (int(t[0]), int(t[1])), (int(t[2]), int(t[3]))
    raise ValueError


def read_move(prompt):
    try:
        return input(prompt).strip().lower()
    except EOFError:
        return "q"
    except KeyboardInterrupt:
        return "q"


def main():
    game = Game()
    print("=== Match-3 ===  Line up 3+ candies to clear them.")
    print("Move: 'row col u/d/l/r' (e.g. 3 2 r) or 'r1 c1 r2 c2'. 'h' hint, 'q' quit.")
    while not game.over:
        draw(game)
        raw = read_move("move> ")
        if raw in ("q", "quit", "exit"):
            print("Thanks for playing!")
            return
        if raw == "h":
            mv = game.board.find_move()
            print(f"Hint: swap {mv[0]} with {mv[1]}.")
            continue
        try:
            a, b = parse(raw)
            print(game.move(a, b))
        except (ValueError, IndexError):
            print("Invalid input.")
    draw(game)
    print("*** YOU WIN! ***" if game.score >= game.TARGET else "*** OUT OF MOVES - GAME OVER ***")
    print(f"Final score: {game.score}")


if __name__ == "__main__":
    main()