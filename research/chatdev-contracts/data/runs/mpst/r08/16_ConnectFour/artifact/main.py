'''
main.py
Entry point for the Connect Four application.
Collects optional player names, runs full games in a loop, and offers
a rematch after each game until the players choose to quit.
'''
from game import Game
from player import Player
def ask_name(default, symbol):
    """Prompt for a player's name, falling back to the default when empty."""
    raw = input("Name for {} ({}): ".format(default, symbol)).strip()
    return raw if raw else default
def main():
    """Create the players and run Connect Four games until the user quits."""
    print("=== Connect Four ===")
    name_one = ask_name("Player 1", "X")
    name_two = ask_name("Player 2", "O")
    while True:
        game = Game(Player(name_one, "X"), Player(name_two, "O"))
        game.play()
        again = input("Play again? (y/n): ").strip().lower()
        if again != 'y':
            print("Thanks for playing Connect Four. Goodbye!")
            break
if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nGame interrupted. Goodbye!")