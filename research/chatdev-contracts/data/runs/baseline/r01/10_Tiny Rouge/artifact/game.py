    def new_game(self):
        """Reset all state and build level 1."""
        self.level = 1
        self.player = Player(0, 0, max_hp=PLAYER_START_HP, hp=PLAYER_START_HP)
        self.messages = []
        self._build_level()
        self.state = "playing"
        self.held.clear()