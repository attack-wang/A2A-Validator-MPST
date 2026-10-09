'''
main.py
Entry point for the Reversi (Othello) game. Creates the game and GUI and
starts the main loop.
'''
from gui import GameGUI
def main():
    gui = GameGUI()
    gui.run()
if __name__ == "__main__":
    main()