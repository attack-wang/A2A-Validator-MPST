'''
Main entry point for the Gomoku game.
Wires together the game logic (Game) and the graphical interface
(GomokuGUI), then starts the tkinter event loop so the user can play.
'''
from game import Game
from gui import GomokuGUI
def main():
    '''Create the game logic and its GUI, then launch the application.'''
    game = Game()          # Core match flow: turns, moves, win/draw detection
    gui = GomokuGUI(game)  # Tkinter window bound to the game instance
    gui.run()              # Start the tkinter main loop (blocks until closed)
if __name__ == "__main__":
    main()