"""Connect Four: two-player game on a 7-column, 6-row grid."""

ROWS = 6
COLS = 7
EMPTY = " "
DISCS = ("X", "O")


def create_board():
    """Return a new empty Connect Four board."""
    return [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board):
    """Display the board with column numbers."""
    print("\n " + " ".join(str(c + 1) for c in range(COLS)))
    print("+" + "-" * (2 * COLS - 1) + "+")
    for row in board:
        print("|" + "|".join(row) + "|")
    print("+" + "-" * (2 * COLS - 1) + "+")


def drop_row(board, col):
    """Return the lowest empty row in col, or None if the column is full."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == EMPTY:
            return row
    return None


def is_valid_move(board, col):
    """A move is valid when the column exists and is not full."""
    return 0 <= col < COLS and drop_row(board, col) is not None


def drop_disc(board, col, disc):
    """Place disc in col and return the row it landed in."""
    row = drop_row(board, col)
    board[row][col] = disc
    return row


def is_winning_move(board, row, col, disc):
    """Return True if the disc at (row, col) completes a line of four."""
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


def board_full(board):
    """Return True when every column is full (draw)."""
    return all(board[0][col] != EMPTY for col in range(COLS))


def ask_column(board, player):
    """Prompt until the player enters a valid, non-full column number."""
    while True:
        raw = input(f"Player {player}, choose a column (1-{COLS}): ").strip()
        if not raw.isdigit():
            print("Invalid input: please type a number.")
            continue
        col = int(raw) - 1
        if not 0 <= col < COLS:
            print(f"Out of range: pick a column from 1 to {COLS}.")
            continue
        if not is_valid_move(board, col):
            print("That column is full: pick another one.")
            continue
        return col


def play():
    """Run one full game of Connect Four."""
    board = create_board()
    print("Welcome to Connect Four! Line up four discs to win.")
    print_board(board)
    turn = 0
    while True:
        player = DISCS[turn % 2]
        col = ask_column(board, player)
        row = drop_disc(board, col, player)
        print_board(board)
        if is_winning_move(board, row, col, player):
            print(f"Player {player} wins! Four in a row.")
            return
        if board_full(board):
            print("It's a draw: the grid is full.")
            return
        turn += 1


if __name__ == "__main__":
    try:
        play()
    except EOFError:
        print("\nInput stream closed: Connect Four session ended.")