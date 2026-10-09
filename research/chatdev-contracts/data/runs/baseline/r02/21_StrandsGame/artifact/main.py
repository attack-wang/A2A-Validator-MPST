def run_puzzle(puzzle, ui):
    validator = MergeValidator(BONUS_WORDS)
    game = StrandsGame(puzzle, validator)
    while True:
        ui.clear()
        print(ui.render(game.get_state()))
        if game.finished:
            print(ui.celebration(game.get_state()))
            input("\nPress Enter to continue... ")
            return True  # completed
        raw = input("\nCommand (> number to toggle strands, 's' to submit): ")
        result = process_command(game, ui, raw)
        if result is None: continue
        kind, text = result
        if kind == 'QUIT':
            return False  # abort
        if kind == 'RESTART':
            return 'restart'  # signal restart
        if kind == 'HELP':
            print(text); input("Press Enter to continue... ")