"""Reversi (Othello) two-player command-line game."""

from board import Board, EMPTY, BLACK, WHITE

SYMBOLS = {EMPTY: ".", BLACK: "X", WHITE: "O"}
NAMES = {BLACK: "Black (X)", WHITE: "White (O)"}


def render(board, moves):
    header = "  " + " ".join("abcdefgh")
    lines = [header]
    for r in range(8):
        row = []
        for c in range(8):
            if (r, c) in moves:
                row.append("*")
            else:
                row.append(SYMBOLS[board.grid[r][c]])
        lines.append(f"{r + 1} " + " ".join(row))
    print("\n".join(lines))


def parse_move(text):
    text = text.strip().lower()
    if len(text) == 2 and text[0] in "abcdefgh" and text[1] in "12345678":
        return int(text[1]) - 1, "abcdefgh".index(text[0])
    return None


def main():
    board = Board()
    player = BLACK
    passes = 0
    while not board.game_over():
        moves = board.valid_moves(player)
        b, w = board.score()
        print(f"\nScore - Black: {b}  White: {w}")
        render(board, set(moves))
        if not moves:
            passes += 1
            print(f"{NAMES[player]} has no valid move and passes.")
            player = 3 - player
            continue
        passes = 0
        while True:
            try:
                text = input(f"{NAMES[player]} move (e.g. d3, or 'q' to quit): ")
            except EOFError:
                return
            if text.strip().lower() in ("q", "quit"):
                print("Game aborted.")
                return
            move = parse_move(text)
            if move in moves:
                board.place(*move, player)
                break
            print("Invalid move, try again.")
        player = 3 - player
    b, w = board.score()
    render(board, set())
    print(f"\nFinal score - Black: {b}  White: {w}")
    if b > w:
        print("Black wins!")
    elif w > b:
        print("White wins!")
    else:
        print("It's a draw!")


if __name__ == "__main__":
    main()