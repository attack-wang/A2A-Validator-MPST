"""Gomoku (five-in-a-row) console game. Run: python main.py"""

from gomoku import Board, BLACK, WHITE


def parse_move(text, size):
    """Parse 'H8' or 'row col' (e.g. '8 8') input -> 0-based (row, col) or None."""
    tokens = text.replace(",", " ").split()
    if len(tokens) == 1 and len(tokens[0]) >= 2:
        col_char, row_part = tokens[0][0], tokens[0][1:]
        if col_char.isalpha() and row_part.isdigit():
            col = ord(col_char.upper()) - ord("A")
            row = int(row_part) - 1
            if 0 <= row < size and 0 <= col < size:
                return row, col
        return None
    if len(tokens) == 2 and all(t.isdigit() for t in tokens):
        row, col = int(tokens[0]) - 1, int(tokens[1]) - 1
        if 0 <= row < size and 0 <= col < size:
            return row, col
    return None


def main():
    board = Board()
    players = ((BLACK, "Black"), (WHITE, "White"))
    turn = 0
    print("=== Gomoku (15x15, five in a row wins) ===")
    print("Black moves first. Enter moves as 'H8' or 'row col' (e.g. '8 8').")
    print("Type 'quit' to exit.\n")
    while True:
        print(board.render())
        stone, name = players[turn]
        try:
            raw = input(f"{name} ({stone}), your move: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nGame aborted. Goodbye!")
            return
        if raw in ("quit", "exit", "q"):
            print("Game aborted. Goodbye!")
            return
        move = parse_move(raw, board.size)
        if move is None:
            print("Invalid input. Use a column letter A-O plus row 1-15 (e.g. H8), or 'row col'.\n")
            continue
        row, col = move
        if not board.place(row, col, stone):
            print("That cell is occupied or off the board. Try again.\n")
            continue
        line = board.winning_line(row, col)
        if line:
            print(board.render(highlight=set(line)))
            print(f"\n*** {name} ({stone}) wins with five in a row! ***")
            return
        if board.is_full():
            print(board.render())
            print("\n*** The board is full: it's a draw! ***")
            return
        turn = 1 - turn


if __name__ == "__main__":
    main()