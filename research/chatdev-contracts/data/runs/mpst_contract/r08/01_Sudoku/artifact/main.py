"""Classic 9x9 Sudoku — command-line edition.

Run:  python main.py
Commands during play:
    <row> <col> <value>   place a digit (e.g. 3 5 7); value 0 clears the cell
    check                 report mistake cells
    hint                  fill one empty/incorrect cell correctly
    solve                 reveal the full solution
    new                   start a fresh puzzle
    quit                  exit the game
"""

from sudoku import SudokuBoard

PROMPT = "\nCommand (row col value | check | hint | solve | new | quit): "


def render(board):
    lines = ["", "    1 2 3   4 5 6   7 8 9", "  +-------+-------+-------+"]
    for r in range(9):
        row = ["|"]
        for c in range(9):
            row.append(str(board.grid[r][c]) if board.grid[r][c] else ".")
            if c in (2, 5):
                row.append("|")
        row.append("|")
        lines.append(f"{r + 1} " + " ".join(row))
        if r in (2, 5):
            lines.append("  +-------+-------+-------+")
    lines.append("  +-------+-------+-------+")
    return "\n".join(lines)


def report_mistakes(board):
    rule = board.conflicts()
    vs = board.wrong_vs_solution()
    if not rule and not vs:
        print("No mistakes so far — looking good!")
        return
    if rule:
        cells = ", ".join(f"({r + 1},{c + 1})" for r, c in rule)
        print(f"Rule conflicts (duplicate in row/column/box): {cells}")
    if vs:
        cells = ", ".join(f"({r + 1},{c + 1})" for r, c in vs)
        print(f"Values that differ from the solution: {cells}")


def hint(board):
    targets = [(r, c) for r in range(9) for c in range(9)
               if not board.given[r][c] and board.grid[r][c] != board.solution[r][c]]
    if not targets:
        return False
    r, c = targets[0]
    board.grid[r][c] = board.solution[r][c]
    print(f"Hint: cell ({r + 1},{c + 1}) is now {board.solution[r][c]}.")
    return True


def congratulate():
    print("PUZZLE COMPLETE! Every row, column and 3x3 box contains the digits "
          "1-9 exactly once. Congratulations!")


def main():
    print("=== Classic Sudoku (9x9) ===")
    board = SudokuBoard()
    print(render(board))
    while True:
        try:
            raw = input(PROMPT).strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            return
        if raw in ("quit", "exit", "q"):
            print("Thanks for playing!")
            return
        if raw == "new":
            board = SudokuBoard()
            print("New puzzle started.")
            print(render(board))
            continue
        if raw == "solve":
            board.reveal()
            print(render(board))
            print("Solution revealed. Type 'new' for a fresh puzzle or 'quit' to exit.")
            continue
        if raw == "check":
            report_mistakes(board)
            continue
        if raw == "hint":
            if not hint(board):
                print("No hint available (board is already correct).")
            else:
                print(render(board))
                if board.is_complete():
                    congratulate()
            continue
        parts = raw.replace(",", " ").split()
        if len(parts) != 3 or not all(p.isdigit() for p in parts):
            print("Invalid command. Use: row col value (e.g. '3 5 7'), "
                  "or check/hint/solve/new/quit.")
            continue
        r, c, v = (int(p) for p in parts)
        try:
            if not board.place(r - 1, c - 1, v):
                print(f"Cell ({r},{c}) is a given clue and cannot be changed.")
                continue
        except ValueError as err:
            print(err)
            continue
        print(render(board))
        if board.is_complete():
            congratulate()
            again = input("Play again? (y/n): ").strip().lower()
            if again.startswith("y"):
                board = SudokuBoard()
                print(render(board))
            else:
                print("Thanks for playing!")
                return
        else:
            bad = board.conflicts()
            if bad:
                cells = ", ".join(f"({a + 1},{b + 1})" for a, b in bad)
                print(f"Warning: rule conflict at {cells}. Type 'check' for details.")


if __name__ == "__main__":
    main()