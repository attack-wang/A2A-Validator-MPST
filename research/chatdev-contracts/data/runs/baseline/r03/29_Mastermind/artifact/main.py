'''
main.py
Entry point for the Mastermind code-breaking game.
'''
from config import DIFFICULTIES, DEFAULT_DIFFICULTY_KEY
from game import MastermindGame
from ui import banner
def choose_difficulty():
    """Prompt for a difficulty preset and return the chosen Difficulty."""
    print(banner())
    for key, d in DIFFICULTIES.items():
        print(f"  [{key}] {d.name:<8} code={d.code_length} colors={d.palette_size} "
              f"attempts={d.max_attempts} duplicates={'yes' if d.allow_duplicates else 'no'}")
    while True:
        choice = input(f"Choice [{DEFAULT_DIFFICULTY_KEY}]: ").strip() or DEFAULT_DIFFICULTY_KEY
        if choice in DIFFICULTIES:
            return DIFFICULTIES[choice]
        print("Invalid choice — enter 1, 2, or 3.")
def main():
    """Entry point: difficulty selection, game rounds, replay loop."""
    while True:
        MastermindGame(choose_difficulty()).play()
        if input("Play again? [y/N]: ").strip().lower() not in ("y", "yes"):
            print("Thanks for playing — goodbye!")
            break
if __name__ == "__main__":
    main()