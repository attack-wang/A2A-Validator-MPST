"""Connect Four - a two-player console game."""


ROWS, COLS = 6, 7
EMPTY = "."


def new_board():
    """Create an empty Connect Four board."""
    return [[EMPTY] * COLS for _ in range(ROWS)]


def print_board(board):
    """Display the board with column numbers beneath it."""
    for row in board:
        print(" ".join(row))
    print(" ".join(str(c + 1) for c in range(COLS)))


def drop_disc(board, col, disc):
    """Place a disc in the given column; return its row, or -1 if full."""
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == EMPTY:
            board[r][col] = disc
            return r
    return -1


def is_full(board):
    """Return True when the board has no empty cells left."""
    return all(board[0][c] != EMPTY for c in range(COLS))


def winning_line(board, row, col, disc):
    """Check all directions from the last move for four in a row."""
    directions = ((0, 1), (1, 0), (1, 1), (1, -1))
    for dr, dc in directions:
        count = 1
        for sign in (1, -1):
            r, c = row + dr * sign, col + dc * sign
            while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == disc:
                count += 1
                r += dr * sign
                c += dc * sign
        if count >= 4:
            return True
    return False


def get_move(board, player):
    """Prompt until the player enters a valid, non-full column."""
    while True:
        try:
            line = input(f"Player {player}, choose a column (1-{COLS}): ").strip()
        except EOFError:
            print("\nInput stream closed. Exiting Connect Four.")
            raise SystemExit(0)
        except KeyboardInterrupt:
            print("\nInterrupted. Goodbye!")
            raise SystemExit(130)
        try:
            col = int(line) - 1
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
        if not 0 <= col < COLS:
            print(f"Column must be between 1 and {COLS}.")
        elif board[0][col] != EMPTY:
            print("That column is full. Choose another.")
        else:
            return col


def main():
    board = new_board()
    players = ("X", "O")
    turn = 0
    print("Welcome to Connect Four! Connect four discs to win.")
    print_board(board)
    while True:
        player = players[turn % 2]
        col = get_move(board, player)
        row = drop_disc(board, col, player)
        print_board(board)
        if winning_line(board, row, col, player):
            print(f"Player {player} wins!")
            break
        if is_full(board):
            print("It's a draw!")
            break
        turn += 1


if __name__ == "__main__":
    main()