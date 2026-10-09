def play(self):
    self.show_welcome()
    while not self.game_over:
        self.round_number += 1
        self.show_round_header()
        for player in list(self.players):
            if player.bankrupt:
                continue
            self.take_turn(player)
            if self.check_game_over():
                break
        # round end
    self.declare_winner()