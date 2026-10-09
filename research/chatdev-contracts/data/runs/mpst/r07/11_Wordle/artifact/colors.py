'''
colors.py
Terminal color constants and small rendering helpers for the Wordle game.
Uses standard ANSI escape sequences so the game runs in any Linux
terminal without external dependencies. Also defines the feedback
codes (GREEN / YELLOW / GREY) shared by the validator and the board
renderer, and maps them to colored "tiles" for display.
'''
class Colors:
    ...