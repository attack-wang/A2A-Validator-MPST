'''
main.py
Entry point for the Mastermind code-breaking game.
Wires together the game engine (game.MastermindGame) and the console
user interface (ui.ConsoleUI), lets the player choose a difficulty,
runs complete game sessions, and supports replaying.
'''
from game import MastermindGame
from ui import ConsoleUI
from colors import enable_windows_ansi
# Difficulty presets: key -> (name, configuration for MastermindGame)
DIFFICULTY_PRESETS = {
    "1": ("Easy",   {"code_length": 4, "palette_size": 6, "max_attempts": 12}),
    "2": ("Medium", {"code_length": 4, "palette_size": 6, "max_attempts": 10}),
    "3": ("Hard",   {"code_length": 5, "palette_size": 7, "max_attempts": 10}),
    "4": ("Expert", {"code_length": 6, "palette_size": 7, "max_attempts": 12}),
}
def choose_difficulty():
    """Prompt the player to pick a difficulty; returns (name, config)."""
    print("Select a difficulty:")
    for key, (name, config) in DIFFICULTY_PRESETS.items():
        print(f"  {key}) {name:<7} - code of {config['code_length']} colors, "
              f"{config['palette_size']} colors in palette, "
              f"{config['max_attempts']} attempts")
    while True:
        choice = input("Your choice [1-4] (default 2): ").strip()
        if choice == "":
            choice = "2"
        if choice in DIFFICULTY_PRESETS:
            return DIFFICULTY_PRESETS[choice]
        print("Invalid choice — please enter 1, 2, 3 or 4.")
def run_session(game, ui):
    """Play one full game session (until win, loss, or forfeit)."""
    ui.show_board()
    while not game.is_over():
        ui.show_round_header()
        guess = ui.get_guess()
        if guess is None:          # player chose to give up
            game.forfeit()         # mark the game finished before leaving
            ui.show_forfeit()
            return
        game.make_guess(guess)
        ui.show_board()
    if game.is_won():
        ui.show_win()
    else:
        ui.show_lose()
def main():
    """Top-level loop: difficulty selection, game sessions, replay."""
    enable_windows_ansi()
    print("Welcome to Mastermind — the classic code-breaking game!\n")
    while True:
        _, config = choose_difficulty()
        game = MastermindGame(**config)
        ui = ConsoleUI(game)
        ui.show_welcome()
        run_session(game, ui)
        if not ui.ask_play_again():
            break
        print()  # spacing before the next game
    print("Thanks for playing Mastermind. Goodbye!")
if __name__ == "__main__":
    main()