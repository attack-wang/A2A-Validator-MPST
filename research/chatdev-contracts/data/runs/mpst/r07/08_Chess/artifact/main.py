def main():
    game = Game()
    print welcome
    display board
    while True:
        current = game.turn
        status = game.status()  # checkmate/stalemate/draw checks
        if status: print result; break
        prompt = f"{name} to move (in check!)" if in check
        user_input = input(prompt)
        handle commands or parse move
        if move valid: apply, print move made, board, check announcements