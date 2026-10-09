'''
main.py
Entry point of the Gomoku application. Creates the Game instance,
attaches the tkinter GUI to it and starts the event loop.
'''
from game import Game
from gui import GomokuGUI
def main():
    '''Instantiate the game and launch its graphical interface.'''
    game = Game()
    gui = GomokuGUI(game)
    gui.run()
if __name__ == "__main__":
    main()