'''
main.py
Entry point of the 2048 game. Wires the pure game logic (Game2048) to
the tkinter presentation layer (GameUI). The UI owns the tkinter event
loop; moves are applied directly on key presses and the board is
redrawn after every state change, so no external game loop is needed.
'''
from game_logic import Game2048
from ui import GameUI
def main():
    '''Create the game and UI objects and start the tkinter main loop.'''
    game = Game2048()
    ui = GameUI(game)
    ui.run()
if __name__ == '__main__':
    main()