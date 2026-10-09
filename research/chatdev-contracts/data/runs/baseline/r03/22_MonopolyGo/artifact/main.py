'''
main.py
Entry point for the simplified Monopoly Go! game. Collects player names,
creates the Game instance and starts the game loop.
'''
import sys
from game import Game
def get_player_names():
    '''Prompt until 2-4 valid player names are entered.'''
    while True:
        raw = input("Enter player names separated by commas (2-4 players): ").strip()
        names = [n.strip() for n in raw.split(",") if n.strip()][:4]
        if len(names) >= 2:
            return names
        print("Please enter at least 2 valid names (maximum 4).")
def main():
    '''Entry point: get player names, create game, run it.'''
    print("=== Simplified Monopoly Go! ===")
    names = get_player_names()
    game = Game(names)
    try:
        game.play()
    except KeyboardInterrupt:
        print("\nGame interrupted. Goodbye!")
        sys.exit(0)
if __name__ == "__main__":
    main()