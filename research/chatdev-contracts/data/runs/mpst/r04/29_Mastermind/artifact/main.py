'''
Entry point for the Mastermind game.
Wires the GameEngine and ConsoleUI together and runs the outer loop:
one full game per iteration, with a replay prompt at the end of each.
Run this file directly to play:  python main.py
'''
from engine import GameEngine, GuessValidationError
from ui import ConsoleUI
def main():
    """Run complete games until the player declines a replay."""
    while True:
        engine = GameEngine()
        ui = ConsoleUI(engine)
        ui.show_welcome()
        while not engine.is_over:
            ui.show_turn_banner()
            raw = ui.prompt_guess()
            if raw is None:                 # EOF / Ctrl+C — abort gracefully
                print("\nGame aborted. Secret code was:",
                      engine.secret_revealed())
                return
            try:
                feedback = engine.submit_guess(raw)
            except GuessValidationError as exc:
                ui.show_error(str(exc))
                continue                    # invalid guesses don't consume attempts
            ui.show_feedback(feedback)
            ui.show_board()
        if engine.won:
            ui.show_win()
        else:
            ui.show_lose()
        if not ui.ask_replay():
            break
    print("\nThanks for playing Mastermind. Goodbye!")
if __name__ == "__main__":
    main()