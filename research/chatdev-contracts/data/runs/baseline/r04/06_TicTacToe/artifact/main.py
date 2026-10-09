'''
Main entry point for the Tic-Tac-Toe game.
This module starts the application, runs complete rounds of the game,
keeps a simple scoreboard across rounds (keyed by name AND symbol so
identical names never merge into one entry), asks whether the players
want to play again, and handles KeyboardInterrupt/EOFError gracefully.
'''
from game import Game
def main():
    """Run the Tic-Tac-Toe application with replay and score tracking."""
    scores = {}
    print("Starting Tic-Tac-Toe...")
    try:
        while True:
            game = Game()
            winner = game.play()
            if winner is not None:
                # Key by (name, symbol) so two different players who share
                # the same name are never merged into one scoreboard entry.
                key = (winner.name, winner.symbol)
                scores[key] = scores.get(key, 0) + 1
            if scores:
                print("\n--- Scoreboard ---")
                for (name, symbol), wins in sorted(
                    scores.items(), key=lambda item: -item[1]
                ):
                    print(f"{name} ({symbol}): {wins} win(s)")
                print("------------------")
            replay = input("\nPlay another round? (y/n): ").strip().lower()
            if replay != "y":
                print("Thanks for playing Tic-Tac-Toe. Goodbye!")
                break
    except (KeyboardInterrupt, EOFError):
        # Graceful exit on Ctrl+C or closed input stream instead of a traceback.
        print("\nGame interrupted. Thanks for playing Tic-Tac-Toe. Goodbye!")
if __name__ == "__main__":
    main()