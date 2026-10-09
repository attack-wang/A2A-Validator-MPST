'''
console.py
Text-based fallback front-end for the Reversi (Othello) game.
Used automatically when the pygame module is unavailable. It reuses the
exact same Board and Game rule engine as the GUI: valid moves are shown
with '*', discs are flipped automatically, the live score is displayed
after every move, a player with no move passes automatically and the
final result is announced when the game ends.
'''
from constants import BOARD_SIZE, BLACK, WHITE, PLAYER_NAMES
from game import Game
def format_board(game):
    '''Return a multi-line string with the board, valid-move markers
    ('*') and the current score.'''
    score = game.get_score()
    valid_moves = set() if game.game_over else set(game.get_valid_moves())
    lines = ["   " + " ".join(chr(ord('A') + c) for c in range(BOARD_SIZE))]
    for r in range(BOARD_SIZE):
        cells = []
        for c in range(BOARD_SIZE):
            disc = game.board.get_disc(r, c)
            if disc == BLACK:
                cells.append("B")
            elif disc == WHITE:
                cells.append("W")
            elif (r, c) in valid_moves:
                cells.append("*")
            else:
                cells.append(".")
        lines.append(f"{r + 1}  " + " ".join(cells))
    lines.append("")
    lines.append(f"Score - Black: {score[BLACK]}  White: {score[WHITE]}")
    return "\n".join(lines)
def parse_move(text):
    '''Convert input such as "D3" into (row, col); None when malformed.'''
    text = text.strip().upper()
    if len(text) == 2 and text[0].isalpha() and text[1].isdigit():
        col = ord(text[0]) - ord('A')
        row = int(text[1]) - 1
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            return row, col
    return None
def run_console_game():
    '''Run the interactive console loop until the game ends or the user
    quits with q/quit/exit.'''
    game = Game()
    print("=== Reversi (Othello) - console mode ===")
    print("Enter moves as column+row, e.g. D3. '*' marks your valid moves. "
          "Type 'q' to quit.")
    while not game.game_over:
        print(format_board(game))
        print(game.message)
        try:
            move_text = input(f"{PLAYER_NAMES[game.current_player]}, your move: ")
        except (EOFError, KeyboardInterrupt):
            print("\nGame aborted.")
            return
        if move_text.strip().lower() in ("q", "quit", "exit"):
            print("Game aborted.")
            return
        cell = parse_move(move_text)
        if cell is None:
            print("Bad input - use a letter A-H followed by a number 1-8 "
                  "(e.g. D3).\n")
            continue
        row, col = cell
        if not game.make_move(row, col):
            print(f"{game.message}\n")
    print(format_board(game))
    score = game.get_score()
    if game.winner is None:
        print(f"Game over - it's a draw! Final score: "
              f"Black {score[BLACK]} - {score[WHITE]} White")
    else:
        print(f"Game over - {PLAYER_NAMES[game.winner]} wins! "
              f"Final score: Black {score[BLACK]} - {score[WHITE]} White")