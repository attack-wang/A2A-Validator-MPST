from game import TicTacToe


def main():
    while True:
        game = TicTacToe()
        game.play()
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing! Goodbye.")
            break


if __name__ == "__main__":
    main()