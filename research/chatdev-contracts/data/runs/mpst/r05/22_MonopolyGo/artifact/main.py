from ui import get_choice, get_line
from game import Game
def get_player_count():
    while True:
        raw = get_line("How many players (2-4)? ")
        try:
            num = int(raw)
        except ValueError:
            print("Please enter a number between 2 and 4.")
            continue
        if 2 <= num <= 4:
            return num
        print("Please enter a number between 2 and 4.")
def main():
    print("=" * 50)
    print("   WELCOME TO SIMPLIFIED MONOPOLY GO!")
    print("=" * 50)
    num = get_player_count()
    names = []
    for i in range(num):
        name = get_line(f"Player {i + 1} name: ") or f"Player {i + 1}"
        names.append(name)
    game = Game(names)
    game.play()
if __name__ == "__main__":
    main()