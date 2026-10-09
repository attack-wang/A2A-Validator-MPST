'''
Console (text-based) fallback version of Reversi (Othello), used when
pygame is not installed. It renders the board in the terminal, lists the
valid moves for the current player, reads moves from the keyboard,
automatically flips opponent discs, handles passes, and reports the
running and final score, mirroring the rules in game_logic.py.
'''
from game_logic import ReversiGame
PLAYER_NAMES = {ReversiGame.BLACK: "Black", ReversiGame.WHITE: "White"}
DISC_SYMBOLS = {ReversiGame.EMPTY: ".", ReversiGame.BLACK: "B", ReversiGame.WHITE: "W"}
def print_board(game):
    '''Print the current board with column and row labels.'''
    header = "   " + " ".join(str(col) for col in range(ReversiGame.BOARD_SIZE))
    print(header)
    for row in range(ReversiGame.BOARD_SIZE):
        cells = " ".join(
            DISC_SYMBOLS[game.board[row][col]] for col in range(ReversiGame.BOARD_SIZE)
        )
        print(f"{row}  {cells}")
    print()
def format_moves(moves):
    '''Format a list of (row, col) moves into a readable string.'''
    return ", ".join(f"({row},{col})" for row, col in moves)
def read_move(player):
    '''
    Prompt the current player for a move until a syntactically valid
    'row col' pair is entered. Returns (row, col) as integers.
    '''
    while True:
        raw = input(f"{PLAYER_NAMES[player]}, enter move as 'row col' (e.g. '2 3'): ").strip()
        parts = raw.replace(",", " ").split()
        if len(parts) != 2:
            print("Invalid input. Please enter two numbers separated by a space.\n")
            continue
        try:
            row, col = int(parts[0]), int(parts[1])
        except ValueError:
            print("Invalid input. Please enter numeric row and column values.\n")
            continue
        return row, col
def run_console_game():
    '''Run an interactive two-player Reversi game in the terminal.'''
    game = ReversiGame()
    print("Welcome to Reversi (Othello)! Black (B) moves first.\n")
    while not game.is_game_over():
        print_board(game)
        score = game.get_score()
        print(f"Score -> Black: {score[ReversiGame.BLACK]}  White: {score[ReversiGame.WHITE]}")
        player = game.current_player
        moves = game.get_valid_moves(player)
        if not moves:
            # Normally unreachable (turn logic auto-passes), kept for safety.
            print(f"{PLAYER_NAMES[player]} has no valid moves and must pass.\n")
            game.current_player = game.get_opponent(player)
            continue
        print(f"Valid moves: {format_moves(moves)}")
        row, col = read_move(player)
        if game.make_move(row, col, player):
            print()
        else:
            print("Illegal move: it does not flip any opponent disc. Try again.\n")
    print_board(game)
    score = game.get_score()
    print(f"Final score -> Black: {score[ReversiGame.BLACK]}  White: {score[ReversiGame.WHITE]}")
    winner = game.get_winner()
    if winner is None:
        print("The game ended in a tie!")
    else:
        print(f"{PLAYER_NAMES[winner]} wins!")
if __name__ == "__main__":
    run_console_game()