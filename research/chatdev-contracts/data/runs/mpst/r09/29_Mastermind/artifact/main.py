def run_session(engine, ui):
    engine.start()
    while not engine.is_finished:
        ui.display_board(engine)
        guess = ui.get_player_guess(engine)
        if guess is None:
            return False
        feedback = engine.submit_guess(guess)
        ui.display_feedback(feedback, engine)
    ui.display_board(engine)
    if engine.is_won:
        ui.display_win(engine)
    else:
        ui.display_lose(engine)
    return True