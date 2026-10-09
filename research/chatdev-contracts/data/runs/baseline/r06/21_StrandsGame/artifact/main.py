import sys
from game import StrandsGame
from puzzles import PUZZLES, DICTIONARY
from puzzle import Puzzle
from ui import ConsoleUI
def choose_puzzle():
    # list puzzles, let user pick by number, default 1
    ...
def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    definition = choose_puzzle(argv)
    if definition is None:
        return
    puzzle = Puzzle.from_definition(definition, DICTIONARY)
    game = StrandsGame(puzzle)
    game.run()
if __name__ == "__main__":
    main()