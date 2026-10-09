'''
Main entry point: sets up players and starts the Monopoly Go! game loop.
'''
from game import Game
def main():
    """Create a Game from user-chosen player names and run it."""
    print("=" * 62)
    print("  MONOPOLY GO! — simplified console edition")
    print("=" * 62)
    while True:
        raw = input("How many players (2-4)? ").strip()
        if raw in ("2", "3", "4"):
            count = int(raw)
            break
        print("Please enter 2, 3 or 4.")
    names = []
    for i in range(count):
        name = input(f"Player {i + 1} name: ").strip() or f"Player {i + 1}"
        names.append(name)
    game = Game(names)
    game.run()
if __name__ == "__main__":
    main()