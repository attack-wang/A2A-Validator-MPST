'''
main.py
Entry point for the Reversi (Othello) application.
Creates the Game (rules/turn logic) and launches the pygame GUI when the
pygame module is available. If pygame is missing (ModuleNotFoundError,
as reported by the test environment), the program falls back to an
interactive console version so the game always runs smoothly.
'''
from game import Game
def main():
    '''Launch the graphical interface, or the console fallback when
    pygame is not installed in the current environment.'''
    try:
        import pygame  # noqa: F401 - availability probe only
    except ImportError:
        print("pygame is not installed - switching to console mode.")
        print("Tip: run 'pip install pygame' to enable the graphical version.\n")
        from console import run_console_game
        run_console_game()
        return
    from gui import GameGUI
    game = Game()
    gui = GameGUI(game)
    gui.run()
if __name__ == "__main__":
    main()