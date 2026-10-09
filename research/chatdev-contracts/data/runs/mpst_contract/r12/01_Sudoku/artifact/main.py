"""Console entry point for the classic 9x9 Sudoku game."""

from sudoku import SudokuBoard


def ask(prompt, lo, hi, allow_quit=True):
    while True:
        s = input(prompt).strip().lower()
        if allow_quit and s in ("q", "quit"):
            return None
        if s.isdigit() and lo <= int(s) <= hi:
            return int(s)
        suffix = " or 'q' to quit" if allow_quit else ""
        print(f"Please enter a number {lo}-{hi}{suffix}.")


def main():
    print("=== Classic Sudoku (9x9) ===")
    print("Fill every row, column and 3x3 box with the digits 1-9.")
    board = SudokuBoard(clues=38)
    while True:
        print()
        board.display()
        mistakes = board.find_mistakes()
        if mistakes:
            print("Mistakes in cells:",
                  ", ".join(f"(row {r + 1}, col {c + 1})" for r, c in mistakes))
        if board.is_complete():
            print("Congratulations! The puzzle is complete and correct!")
            break
        print("\nCommands: <Enter> = fill a cell, c = clear a cell, q = quit")
        cmd = input("> ").strip().lower()
        if cmd in ("q", "quit"):
            print("Thanks for playing!")
            break
        if cmd == "c":
            r = ask("Row to clear (1-9): ", 1, 9, allow_quit=False)
            c = ask("Column to clear (1-9): ", 1, 9, allow_quit=False)
            if board.is_fixed(r - 1, c - 1):
                print("That cell is a fixed clue and cannot be cleared.")
            else:
                board.clear_cell(r - 1, c - 1)
                print("Cell cleared.")
            continue
        r = ask("Row (1-9): ", 1, 9)
        if r is None:
            break
        c = ask("Column (1-9): ", 1, 9)
        if c is None:
            break
        v = ask("Value (1-9): ", 1, 9)
        if v is None:
            break
        r, c = r - 1, c - 1
        if board.is_fixed(r, c):
            print("That cell is a fixed clue and cannot be changed.")
        elif not board.is_valid_move(r, c, v):
            print(f"Warning: {v} conflicts with its row, column or box; "
                  "it was placed anyway and is flagged as a mistake.")
            board.set_cell(r, c, v)
        else:
            board.set_cell(r, c, v)
            print(f"Placed {v} at (row {r + 1}, col {c + 1}).")


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nGame exited.")