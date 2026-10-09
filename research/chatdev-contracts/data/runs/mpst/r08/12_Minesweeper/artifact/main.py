'''
Entry point for the Minesweeper application.
Creates the main GUI window and starts the Tkinter event loop.
'''
from gui import MinesweeperGUI
def main():
    '''Launch the Minesweeper game.'''
    app = MinesweeperGUI()
    app.mainloop()
if __name__ == "__main__":
    main()