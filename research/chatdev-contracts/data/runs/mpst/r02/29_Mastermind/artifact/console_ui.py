'''
console_ui.py
Text-based user interface for the Mastermind game.
Used as an automatic fallback when tkinter is unavailable, and also as a
lightweight alternative for playing in a terminal.
'''
from game import MastermindGame
def play_console_game():
    '''Run one full game session in the terminal.'''
    game = MastermindGame()
    print header, instructions, palette
    while not game.is_over():
        show attempts remaining
        prompt for guess (comma-separated colors or numbers)
        validate, submit, print feedback
    print win/lose outcome and reveal secret