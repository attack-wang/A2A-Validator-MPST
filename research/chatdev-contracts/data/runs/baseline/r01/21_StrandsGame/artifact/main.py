'''
main.py - Entry point for the Strands word-segmentation puzzle game.
'''
from game import StrandsGame
from puzzles_data import PUZZLES
def main():
    game = StrandsGame(PUZZLES)
    game.run()
if __name__ == "__main__":
    main()