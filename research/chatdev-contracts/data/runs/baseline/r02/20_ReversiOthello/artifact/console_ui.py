'''
console_ui.py
Terminal front-end for the Reversi game: clears the screen, renders the board
with legal moves marked '*', prints the score, parses and validates player
input (algebraic 'd3' or numeric '4 4' style), announces passes and results,
and defines the QuitGame exception raised when the user chooses to leave.
'''
import os
from board import EMPTY, BLACK, WHITE
COLUMN_LABELS = "abcdefgh"
DISC_SYMBOLS = {EMPTY: ".", BLACK: "X", WHITE: "O"}
LEGAL_MOVE_SYMBOL = "*"
QUIT_COMMANDS = ("q", "quit", "exit")
class QuitGame(Exception):
    """Raised when the user types 'q' to leave the game early."""
def clear_screen():
    """Clear the terminal window on Windows and Unix-like systems."""
    os.system("cls" if os.name == "nt" else "clear")
def print_welcome():
    """Show the application banner."""
    print("=" * 46)
    print("         Welcome to Reversi (Othello)!")
    print("=" * 46)
def print_rules_summary():
    """Explain the input format and the board symbols."""
    print("Black (X) moves first. Enter a move as 'd3' or 'row col' (e.g. '4 4').")
    print("Legal moves are marked with '*'. Type 'q' to quit at any prompt.")
def print_board(board, current_player):
    """Render the grid; mark legal moves for `current_player` (None = no marks)."""
    valid = set(board.get_valid_moves(current_player)) if current_player else set()
    print("  " + " ".join(COLUMN_LABELS))
    for r in range(board.SIZE):
        cells = [
            LEGAL_MOVE_SYMBOL if (r, c) in valid else DISC_SYMBOLS[board.grid[r][c]]
            for c in range(board.SIZE)
        ]
        print(f"{r + 1} " + " ".join(cells))
def print_score(board):
    """Show the current disc counts for both colours."""
    black, white = board.count_discs()
    print(f"Score -> Black (X): {black}   White (O): {white}")
def announce_pass(player_name):
    """Tell the user that `player_name` cannot move and must pass."""
    input(f"{player_name} has no legal move and must pass. Press Enter to continue...")
def print_legal_moves(valid_moves):
    """List the legal moves in algebraic form (e.g. 'd3, e6')."""
    coords = ", ".join(f"{COLUMN_LABELS[c]}{r + 1}" for r, c in sorted(valid_moves))
    print(f"Legal moves: {coords if coords else 'none'}")
def parse_move(text, valid_moves):
    """
    Convert user text into a legal (row, col) move.
    Accepts algebraic ('d3') or numeric ('4 4' or '4,4', 1-indexed) input.
    Returns None when the text is not a legal move.
    """
    text = text.strip().lower()
    if not text:
        return None
    valid = set(valid_moves)
    # Algebraic style: "d3" (column letter + row number)
    if len(text) == 2 and text[0] in COLUMN_LABELS and text[1].isdigit():
        candidate = (int(text[1]) - 1, ord(text[0]) - ord("a"))
        return candidate if candidate in valid else None
    # Numeric style: "4 3" or "4,3" -> row 4, column 3 (1-indexed)
    parts = text.replace(",", " ").split()
    if len(parts) == 2 and all(part.isdigit() for part in parts):
        row, col = int(parts[0]) - 1, int(parts[1]) - 1
        candidate = (row, col)
        return candidate if candidate in valid else None
    return None
def prompt_move(player_name, valid_moves):
    """Ask `player_name` for a move until a legal one (or 'q') is entered."""
    while True:
        text = input(f"{player_name}, your move (e.g. d3 / '4 4' / q): ")
        if text.strip().lower() in QUIT_COMMANDS:
            raise QuitGame()
        move = parse_move(text, valid_moves)
        if move is not None:
            return move
        print("Invalid move - please choose one of the squares marked '*'.")
def print_move_result(player_name, move, flipped_count):
    """Confirm the move that was just played and how many discs it flipped."""
    row, col = move
    print(f"{player_name} played {COLUMN_LABELS[col]}{row + 1} "
          f"and flipped {flipped_count} disc(s).")
def pause(message="Press Enter to continue..."):
    """Wait for the user to press Enter (used between turns)."""
    input(message)
def print_final_result(game):
    """Show the final board, the final score and the winner (or a draw)."""
    score = game.get_score()
    black, white = score[BLACK], score[WHITE]
    print("=" * 46)
    print("GAME OVER - final board:")
    print_board(game.board, None)
    print(f"Final score -> Black (X): {black}   White (O): {white}")
    winner = game.get_winner()
    if winner is None:
        print("Result: It's a draw!")
    else:
        name = "Black (X)" if winner == BLACK else "White (O)"
        print(f"Result: {name} wins!")
    print("=" * 46)
def print_early_exit(game):
    """Show the score at the moment the user quits the game."""
    score = game.get_score()
    print("Game ended by user.")
    print(f"Score at exit -> Black (X): {score[BLACK]}   White (O): {score[WHITE]}")
    print("Goodbye!")