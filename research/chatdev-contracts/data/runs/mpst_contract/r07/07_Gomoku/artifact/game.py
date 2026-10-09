"""Turn-based game loop for Gomoku."""


class Game:
    def __init__(self, board, players, ui):
        self.board = board
        self.players = players
        self.ui = ui

    def play(self):
        turn = 0
        while True:
            self.ui.render(self.board)
            player = self.players[turn]
            r, c = self.ui.get_move(player, self.board)
            self.board.place(r, c, player.stone)
            if self.board.check_win(r, c):
                self.ui.render(self.board)
                self.ui.announce_win(player)
                return player
            if self.board.is_full():
                self.ui.render(self.board)
                self.ui.announce_draw()
                return None
            turn ^= 1