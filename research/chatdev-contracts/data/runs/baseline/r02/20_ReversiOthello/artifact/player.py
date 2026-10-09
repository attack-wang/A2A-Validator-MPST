class Player:
    def __init__(self, color, name, is_computer=False):
        ...
    def choose_move(self, board, valid_moves):
        # human: handled by UI; computer: pick best