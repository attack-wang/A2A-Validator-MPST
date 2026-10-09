'''
main.py
Entry point for the Reversi (Othello) game. Creates the Game and GUI
objects and starts the main loop.
'''
from game import Game
from gui import GUI
def main():
    """Set up a new game and launch the graphical interface."""
    game = Game()
    gui = GUI(game)
    gui.run()
if __name__ == "__main__":
    main()