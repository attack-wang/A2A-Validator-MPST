    game = Game(player_names=players, max_rounds=rounds)
    winner = game.play()
    if winner:
        print(f"The winner is {winner.name}!")
    else:
        print("The game ended with no winner.")