"""Reversi (Othello) command-line game."""
from game import Board, SIZE, EMPTY, BLACK, WHITE


def render(board, moves):
    lines = ["  " + " ".join(chr(ord('A') + c) for c in range(SIZE))]
    move_set = set(moves)
    for r in range(SIZE):
        row = []
        for c in range(SIZE):
            cell = board.grid[r][c]
            row.append('*' if cell == EMPTY and (r, c) in move_set else cell)
        lines.append(f"{r + 1} " + " ".join(row))
    return "\n".join(lines)


def parse_move(text):
    text = text.strip().upper()
    if len(text) == 2 and text[0].isalpha() and text[1].isdigit():
        c = ord(text[0]) - ord('A')
        r = int(text[1]) - 1
        if 0 <= r < SIZE and 0 <= c < SIZE:
            return r, c
    return None


def main():
    board = Board()
    player = BLACK
    print("Reversi (Othello) - B goes first. '*' marks valid moves.")
    print("Enter moves as column letter + row number (e.g. 'D3'), or 'Q' to quit.")
    while True:
        moves = board.valid_moves(player)
        black, white = board.score()
        print()
        print(render(board, moves))
        print(f"Score - B: {black}  W: {white}")
        opponent = WHITE if player == BLACK else BLACK
        if not moves:
            if not board.is_full() and board.has_any_move(opponent):
                print(f"Player {player} has no valid move. Turn passes.")
                player = opponent
                continue
            break
        try:
            text = input(f"Player {player}, your move: ")
        except (EOFError, KeyboardInterrupt):
            print()
            return
        if text.strip().upper() == 'Q':
            print("Game aborted.")
            return
        pos = parse_move(text)
        if pos is None or pos not in moves:
            print("Invalid move. Try again.")
            continue
        board.apply_move(player, *pos)
        player = opponent

    black, white = board.score()
    print()
    print(render(board, {}))
    print(f"Final score - B: {black}  W: {white}")
    if black > white:
        print("Black wins!")
    elif white > black:
        print("White wins!")
    else:
        print("It's a tie!")


if __name__ == "__main__":
    main()