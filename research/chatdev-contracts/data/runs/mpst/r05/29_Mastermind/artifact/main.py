'''
main.py
Entry point for the Mastermind game.
Wires together the palette, game engine, and console UI: asks the player
to pick a difficulty, runs the guess loop until the code is cracked or
attempts run out, then reports the outcome and offers to play again.
'''
from colors import ColorPalette
from game import MastermindGame
from ui import ConsoleUI
from config import COLOR_SYMBOLS, COLOR_NAMES, DIFFICULTIES
def choose_difficulty():
    """Prompt until the player picks a valid difficulty key.
    Returns the matching DIFFICULTIES tuple, or None on EOF/interrupt.
    """
    print('Select difficulty:')
    for key in sorted(DIFFICULTIES):
        label, code_length, max_attempts, palette_size = DIFFICULTIES[key]
        print('  [{}] {:<6} - code of {} colors, {} attempts, {} colors to choose from'.format(
            key, label, code_length, max_attempts, palette_size))
    while True:
        try:
            choice = input('Your choice [1/2/3]: ').strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return None
        if choice in DIFFICULTIES:
            return DIFFICULTIES[choice]
        print('  ! Please enter 1, 2, or 3.')
def play_round(settings):
    """Play one full round from setup to outcome. Returns True if won."""
    label, code_length, max_attempts, palette_size = settings
    palette = ColorPalette(COLOR_SYMBOLS[:palette_size], COLOR_NAMES)
    game = MastermindGame(palette, code_length, max_attempts)
    ui = ConsoleUI(palette, code_length, max_attempts)
    ui.show_welcome()
    ui.show_rules()
    while not game.is_over:
        guess = ui.prompt_guess(game)
        if guess is None:
            # Player typed "quit" (or pressed Ctrl-C/Ctrl-D): give up.
            ui.show_outcome(game, gave_up=True)
            return False
        feedback = game.make_guess(guess)
        ui.show_board(game)
        ui.show_feedback(feedback)
    ui.show_outcome(game)
    return game.is_won
def main():
    """Program entry point: difficulty selection and replay loop."""
    while True:
        settings = choose_difficulty()
        if settings is None:
            print('Goodbye!')
            return
        play_round(settings)
        try:
            again = input('\nPlay again? [y/n]: ').strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            return
        if again not in ('y', 'yes'):
            print('Thanks for playing Mastermind. Goodbye!')
            return
if __name__ == '__main__':
    main()