'''
main.py
Entry point of the Connect Four application. It optionally asks for
the players' names, starts the match, and offers a rematch after each
finished game until the players decide to stop.
'''
from game import Game
from player import Player
def ask_player_name(default_name, disc):
    """Ask for a player's name, falling back to the default if empty."""
    name = input(f"Name for {default_name} (plays '{disc}', "
                 f"Enter for default): ").strip()
    return name if name else default_name
def main():
    """Create and run Connect Four matches until the players stop."""
    print("=== Connect Four ===")
    name_one = ask_player_name('Player 1', 'X')
    name_two = ask_player_name('Player 2', 'O')
    while True:
        game = Game(Player(name_one, 'X'), Player(name_two, 'O'))
        finished = game.play()
        if not finished:
            break
        rematch = input("\nPlay again? (y/n): ").strip().lower()
        if rematch not in ('y', 'yes'):
            print("Thanks for playing Connect Four. Goodbye!")
            break
if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nGame interrupted. Goodbye!")