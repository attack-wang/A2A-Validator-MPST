'''
Main entry point for the Classic Snake game.
Initializes the tkinter window and starts the main loop.
Only the Python standard library is required (no pygame).
'''
from game import Game
def main():
    game = Game()
    game.run()
if __name__ == "__main__":
    main()