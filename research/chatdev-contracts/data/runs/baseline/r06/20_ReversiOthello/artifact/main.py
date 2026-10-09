'''
main.py
Entry point for the Reversi (Othello) application.
Creates the Tkinter GUI and the Game object that ties the board
rules to the interface, then hands control over to the GUI event
loop.  Run this file to play:
    python main.py
'''
from game import Game
from gui import Gui
def main():
    """Build the GUI, attach a fresh game to it and start playing."""
    gui = Gui()
    game = Game(gui)
    game.start()
if __name__ == "__main__":
    main()