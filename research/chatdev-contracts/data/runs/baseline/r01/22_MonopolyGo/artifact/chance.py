def move_player(self, player, steps):
    """Move player forward by steps; collect GO salary if passing/landing on GO."""
    dest = (player.position + steps) % self.board.size
    if player.position + steps >= self.board.size:
        self.pay_bank? no — player.receive(Board.GO_SALARY); announce
    player.position = dest