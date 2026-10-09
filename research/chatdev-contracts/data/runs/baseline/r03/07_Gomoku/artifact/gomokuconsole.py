class GomokuConsole:
    SYMBOLS = {Board.EMPTY: ".", Board.BLACK: "X", Board.WHITE: "O"}
    def __init__(self):
        self.game = GomokuGame()
    def print_board(self):
        size = self.game.board.size
        # column header
        header = "    " + " ".join(f"{c % 10}" for c in range(size))
        ...