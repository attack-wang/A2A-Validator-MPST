"""Entry point for the Mastermind code-breaking game."""
from game import MastermindGame


def main():
    while True:
        game = MastermindGame(code_length=4, max_tries=10)
        game.play()
        try:
            again = input("Play again? (y/n): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if again != "y":
            print("Thanks for playing Mastermind. Goodbye!")
            break


if __name__ == "__main__":
    main()