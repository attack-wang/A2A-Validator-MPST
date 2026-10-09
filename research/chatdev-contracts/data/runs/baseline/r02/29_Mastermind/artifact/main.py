def play_one_round(ui):
    attempts = ui.ask_difficulty()
    engine = GameEngine(max_attempts=attempts)
    board = Board()
    ui.show_welcome()
    ui.show_rules()
    while not engine.is_over():
        guess = ui.get_guess(engine.attempts_used + 1, engine.max_attempts)
        if guess == 'quit':
            ui.show_message('\nRound abandoned. The secret code was: {}'.format(
                ui._format_secret(engine.reveal_secret())))
            return True
        ...