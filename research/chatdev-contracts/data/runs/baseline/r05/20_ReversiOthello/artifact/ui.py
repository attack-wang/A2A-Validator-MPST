'''
ui.py
Console user interface for the Reversi (Othello) game.
The ConsoleUI class centralises every interaction with the user:
printing the board, the score and game messages, and reading and
validating the players' moves from standard input.
'''
class ConsoleUI:
    '''Handles all console input and output for the Reversi game.'''
    def display_message(self, message):
        '''Print a message to the console.'''
        print(message)
    def display_board(self, board, valid_moves=None):
        '''Print the current board, marking valid moves with "*".'''
        print()
        print(board.display(valid_moves))
    def display_score(self, board, players):
        '''Print the current disc count for every player.'''
        parts = [f'{player.name} [{player.disc}] = {board.count_discs(player.disc)}'
                 for player in players]
        print('Score: ' + ' | '.join(parts))
    def get_move(self, player, valid_moves):
        '''
        Prompt `player` for a move until a valid one is entered.
        Accepted input is two integers (row and column, 1-8), optionally
        separated by a comma. Entering 'q' or 'quit' returns None, which
        the Game interprets as a request to end the game early.
        '''
        valid_set = set(valid_moves)
        while True:
            raw = input(
                f"{player.name} [{player.disc}] - enter move as 'row col' "
                f"(1-8) or 'q' to quit: "
            ).strip().lower()
            if raw in ('q', 'quit', 'exit'):
                return None
            tokens = raw.replace(',', ' ').split()
            if len(tokens) != 2:
                print("Invalid input. Please enter two numbers, e.g. '3 4'.")
                continue
            try:
                row, col = int(tokens[0]), int(tokens[1])
            except ValueError:
                print('Invalid input. Row and column must be whole numbers.')
                continue
            if not (1 <= row <= 8 and 1 <= col <= 8):
                print('Out of range. Row and column must be between 1 and 8.')
                continue
            move = (row - 1, col - 1)
            if move not in valid_set:
                print('Invalid move. Choose an empty cell marked with "*" '
                      'that captures at least one opponent disc.')
                continue
            return move