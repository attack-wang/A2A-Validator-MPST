"""Entry point for the Mastermind code-breaking game."""
from game import MastermindGame, InputClosed, read_line


def main():
    print("=" * 50)
    print("            MASTERMIND")
    print("=" * 50)
    try:
        while True:
            MastermindGame().play()
            again = read_line("\nPlay again? (y/n): ").strip().lower()
            if again != "y":
                print("Thanks for playing Mastermind. Goodbye!")
                break
    except InputClosed:
        # stdin reached EOF (closed pipe, Ctrl+D/Ctrl+Z): end the session cleanly.
        print("\nInput stream closed. Thanks for playing Mastermind. Goodbye!")
    except KeyboardInterrupt:
        print("\nInterrupted. Thanks for playing Mastermind. Goodbye!")


if __name__ == "__main__":
    main()