class Game:
    def __init__(self):
        self.board = Board()
        self.board.setup()
    def run(self):
        print welcome, rules, commands
        while True:
            print board, status
            if game over: break
            prompt input
            handle commands: 'resign', 'draw', 'help', 'board', 'moves', 'undo'?
            parse SAN, make move, log