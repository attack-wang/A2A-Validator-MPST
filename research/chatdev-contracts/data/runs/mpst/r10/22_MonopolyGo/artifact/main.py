'''
Entry point: set up players and start the simplified Monopoly Go! game.
'''
from game import Game
from utils import prompt_int
def main():
    """Read player setup and run the game."""
    print("Welcome to simplified Monopoly Go!")
    count = prompt_int("How many players (2-4)?", minimum=2, maximum=4)
    names = []
    for i in range(count):
        name = input(f"Enter name for player {i + 1}: ").strip()
        names.append(name if name else f"Player {i + 1}")
    game = Game(names)
    game.play()
if __name__ == "__main__":
    main()