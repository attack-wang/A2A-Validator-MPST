class AIPlayer(Player):
    def choose_bid(self, highest_bid):
        score = self._hand_strength()
        # map score to desired bid
        ...
    def choose_play(self, table):
        if table is free lead:
            # lead with smallest single/pair/etc.
            combos = self._generate_leads()
            pick smallest
        else:
            candidates = self._generate_beats(table.current)
            pick smallest non-bomb; if none, maybe bomb if current leader has few cards or self hand small; else pass