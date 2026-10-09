def print_win(game):
    print()
    print(colorize("🎉 Congratulations! You solved it!", GREEN))
    print("The word was " + colorize(game.target.upper(), GREEN))
    print(f"Solved in {game.attempts_used()}/{game.MAX_ATTEMPTS} attempts.")