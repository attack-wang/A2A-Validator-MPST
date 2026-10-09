'''
main.py
Entry point for the Mastermind game.
Wires configuration, secret generation, the game engine and the console
UI together and runs the full loop:
  1. pick a game mode (colors or digits)
  2. generate the secret code
  3. loop: show history -> prompt guess -> show feedback
  4. show the win/lose outcome
  5. optionally replay, then say goodbye and exit
'''
import sys
from code_generator import SecretCodeGenerator
from game import GameEngine
from game_config import COLOR_MODE, DIGIT_MODE, get_mode_settings
from ui import ConsoleUI
def play_round(ui):
    """Run one complete Mastermind round, from mode choice to outcome."""
    # 1. mode selection and configuration
    mode = ui.prompt_mode([COLOR_MODE, DIGIT_MODE])
    settings = get_mode_settings(mode)
    # 2. build the secret code and the engine that guards it
    generator = SecretCodeGenerator(
        symbols=settings["symbols"],
        code_length=settings["code_length"],
        allow_duplicates=settings["allow_duplicates"],
    )
    engine = GameEngine(
        secret_code=generator.generate(),
        code_length=settings["code_length"],
        max_attempts=settings["max_attempts"],
        valid_symbols=settings["symbols"],
    )
    # 3. main game loop
    ui.show_game_start(mode, settings["symbols"],
                       settings["code_length"], settings["max_attempts"])
    while not engine.is_over():
        ui.show_history(engine.history, settings["code_length"])
        guess = ui.prompt_guess(
            attempt_number=engine.attempts_used + 1,
            max_attempts=engine.max_attempts,
            symbols=settings["symbols"],
            code_length=settings["code_length"],
        )
        feedback = engine.make_guess(guess)
        ui.show_feedback(feedback, settings["code_length"])
    # 4. outcome
    if engine.won:
        ui.show_win(engine.attempts_used, engine.secret_code)
    else:
        ui.show_lose(engine.secret_code)
def main():
    """Run Mastermind sessions until the player quits. Returns exit code."""
    ui = ConsoleUI()
    try:
        while True:
            play_round(ui)
            if not ui.prompt_replay():
                break
    except (EOFError, KeyboardInterrupt):
        print()
        print("Game interrupted. Goodbye!")
        return 1
    except Exception as exc:  # surface any unexpected bug with a clear message
        print(f"Unexpected error: {exc}")
        return 1
    ui.show_goodbye()
    return 0
if __name__ == "__main__":
    sys.exit(main())