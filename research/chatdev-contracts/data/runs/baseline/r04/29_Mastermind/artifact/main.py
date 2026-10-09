'''
main.py
Entry point and game-loop orchestration for the Mastermind game.
Wires the modules together:
  * setup_terminal()    -> enables ANSI colors on every major platform
  * choose_difficulty() -> difficulty selection menu
  * play_round()        -> one complete round (secret code, guesses,
                           exact/partial feedback, win/lose/quit outcome)
  * main()              -> replay loop, difficulty switching, scorekeeping
Input robustness: QuitRoundError (raised on 'quit', EOF or Ctrl-C) is
caught around every menu prompt, so an exhausted or closed stdin ends the
game cleanly with the goodbye message instead of an uncaught traceback.
An optional '--difficulty <key>' command-line flag skips the menu so
automated smoke tests can drive a full round non-interactively.
Run this file directly to start the game:  python main.py
'''
import random
import sys
from board import Board
from cli import CLI, QuitRoundError
from colors import build_palette, setup_terminal
from config import DEFAULT_DIFFICULTY_KEY, DIFFICULTIES
from game_engine import GameEngine
def choose_difficulty(cli):
    """Show the difficulty menu and return the chosen Difficulty preset."""
    return cli.ask_difficulty(DIFFICULTIES)
def play_round(difficulty, rng):
    """Run one full round for the given difficulty.
    Creates a fresh secret code, board and CLI, then loops over player
    guesses until the code is cracked, the attempt budget is spent or the
    player aborts with 'quit'. Returns True when the player wins.
    """
    palette = build_palette(difficulty.palette_size)
    engine = GameEngine(difficulty, rng=rng)
    board = Board(difficulty.code_length, difficulty.max_attempts)
    cli = CLI(palette, difficulty.code_length, difficulty.max_attempts)
    # Remind the player of the (difficulty-specific) colors and feedback.
    cli.show_legend()
    while not engine.is_over():
        # Read a guess; 'quit'/EOF aborts the round, 'help' reprints legend.
        try:
            guess = cli.prompt_guess(engine.attempts_used + 1)
        except QuitRoundError:
            cli.show_quit(engine)
            return False
        # Score the guess against the hidden code (exact + partial matches).
        try:
            exact, partial = engine.evaluate_guess(guess)
        except ValueError as error:
            cli.show_error(str(error))
            continue
        # Record the attempt and show the updated board plus feedback.
        board.add_guess(guess, exact, partial)
        cli.show_board(board)
        cli.show_feedback(exact, partial, engine.attempts_remaining())
        if engine.is_win():
            cli.show_win(engine)
            return True
    # Attempt budget exhausted without a full match -> loss.
    cli.show_lose(engine)
    return False
def parse_difficulty_flag(argv):
    """Extract an optional '--difficulty KEY' from the command line.
    Returns the matching Difficulty preset, or None when the flag is
    absent or does not name a known preset (the interactive menu is used
    in that case).
    """
    for index, arg in enumerate(argv):
        if arg == "--difficulty" and index + 1 < len(argv):
            key = argv[index + 1]
            if key in DIFFICULTIES:
                return DIFFICULTIES[key]
            return None
    return None
def main():
    """Application entry point: banner, rounds, replay and scorekeeping."""
    setup_terminal()
    rng = random.Random()
    # A CLI sized after the default preset drives the menus; its palette is
    # only used for the welcome/legend text, so the default preset is safe.
    default = DIFFICULTIES[DEFAULT_DIFFICULTY_KEY]
    menu_cli = CLI(
        build_palette(default.palette_size),
        default.code_length,
        default.max_attempts,
    )
    menu_cli.show_welcome()
    # Difficulty: command-line flag first (test-friendly), else the menu.
    # EOF / Ctrl-C during any menu prompt ends the session gracefully.
    difficulty = parse_difficulty_flag(sys.argv[1:])
    if difficulty is None:
        try:
            difficulty = choose_difficulty(menu_cli)
        except QuitRoundError:
            menu_cli.show_goodbye(0, 0)
            return
    stats = {"wins": 0, "losses": 0}
    while True:
        won = play_round(difficulty, rng)
        stats["wins" if won else "losses"] += 1
        try:
            choice = menu_cli.ask_play_again()
        except QuitRoundError:
            break
        if choice == "no":
            break
        if choice == "change":
            try:
                difficulty = choose_difficulty(menu_cli)
            except QuitRoundError:
                break
    menu_cli.show_goodbye(stats["wins"], stats["losses"])
if __name__ == "__main__":
    main()