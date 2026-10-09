"""Entry point for simplified Monopoly Go!"""
from game import Game
from constants import MIN_PLAYERS?, MAX_ROUNDS
def main():
    print banner
    while True:
        try:
            count = int(input("How many players (2-4)? "))
            if 2 <= count <= 4:
                break
        except ValueError:
            pass
        print("  Please enter a number between 2 and 4.")
    names = []
    for i in range(count):
        name = input(f"Player {i+1} name: ").strip() or f"Player {i+1}"
        names.append(name)
    game = Game(names)
    game.play()
if __name__ == "__main__":
    main()