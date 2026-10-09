def main():
    print welcome
    game = ChessGame()
    while not game.is_game_over():
        print board
        print turn info, check warning if in check
        move = prompt for input
        handle special commands: help, board, history, resign, quit, moves (list legal moves?)
        try parse & execute
        print result of move (SAN), check announcements
    print final board and result