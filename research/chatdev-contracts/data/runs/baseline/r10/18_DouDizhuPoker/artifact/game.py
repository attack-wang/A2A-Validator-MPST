class Game:
    def __init__(self, player_names, human_index=0):
        ...
    def start(self):
        while True:
            self.setup_round()  # deal, bid
            if self.landlord is None: continue (redeal)
            self.play_phase()
            if not self.play_again(): break