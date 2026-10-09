'''
main.py
Entry point for the Mastermind code-breaking game.
Activates terminal colors, prints the banner, then loops over rounds:
pick a difficulty, build the game engine and player, play the round,
and ask whether to play again. Handles Ctrl+C / EOF gracefully.
'''
import sys
from banner import BANNER
from colors import enable_colors
from game import GameEngine
from player import Player
def main():
    enable_colors()
    print(BANNER)
    while True:
        settings = Player.choose_difficulty()
        engine = GameEngine(**settings)
        player = Player(engine.color_names)
        engine.play(player)
        if not Player.wants_replay():
            break
    print("Thanks for playing Mastermind! Goodbye.")
if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nGame interrupted. Goodbye!")
        sys.exit(0)