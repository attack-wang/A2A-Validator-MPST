run():
    show welcome
    while not game_over:
        round_number += 1
        show round banner
        for player in active_players:
            if player.bankrupt: continue
            take_turn(player)
            if check_game_over(): break
    show results