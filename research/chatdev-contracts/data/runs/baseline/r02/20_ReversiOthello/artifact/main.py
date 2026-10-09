'''
main.py
Entry point for the Reversi (Othello) console application. It wires the game
logic (board.py / game.py) to the terminal front-end (console_ui.py) and runs
the main loop: render the board and the score, ask the current player for a
legal move (passing automatically when stuck), apply the move so discs flip
automatically, switch turns, and stop when the board is full or no valid
moves remain, then announce the final result.
'''
from board import BLACK, WHITE
from game import Game
import console_ui as ui
from console_ui import QuitGame
PLAYER_NAMES = {BLACK: "Black (X)", WHITE: "White (O)"}
def play():
    """Run one complete Reversi game in the terminal."""
    game = Game()
    ui.print_welcome()
    ui.print_rules_summary()
    ui.pause("Press Enter to start the game...")
    quit_requested = False
    while not game.is_game_over():
        board = game.board
        ui.clear_screen()
        ui.print_board(board, game.current_player)
        ui.print_score(board)
        if not game.has_valid_move():
            ui.announce_pass(PLAYER_NAMES[game.current_player])
            game.switch_turn()          # current player passes; opponent moves
            continue
        valid_moves = board.get_valid_moves(game.current_player)
        ui.print_legal_moves(valid_moves)
        try:
            move = ui.prompt_move(PLAYER_NAMES[game.current_player], valid_moves)
        except QuitGame:
            quit_requested = True
            break
        mover = PLAYER_NAMES[game.current_player]   # capture before the turn flips
        flipped = game.apply_move(*move)
        ui.print_move_result(mover, move, len(flipped))
        ui.pause()
    ui.clear_screen()
    if quit_requested:
        ui.print_early_exit(game)
    else:
        ui.print_final_result(game)
if __name__ == "__main__":
    play()