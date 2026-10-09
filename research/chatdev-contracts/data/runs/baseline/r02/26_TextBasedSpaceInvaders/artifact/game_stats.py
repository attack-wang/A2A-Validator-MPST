    def reset_stats(self):
        '''(Re)set the stats that change during one game session.'''
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.game_active = False
        self.game_won = False
        self.game_over = False