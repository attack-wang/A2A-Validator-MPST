    def shuffle(self):
        """Reshuffle existing candy types until there are no matches and at least one move."""
        for _ in range(SHUFFLE_ATTEMPTS):
            types = [candy.type_index for row in self.grid for candy in row]
            random.shuffle(types)
            it = iter(types)
            for r in range(self.rows):
                for c in range(self.cols):
                    self.grid[r][c].type_index = next(it)
            if not self.find_match_groups() and self.find_possible_moves():
                return True
        # Fallback: regenerate a fresh board if reshuffling never produced a valid layout
        self.generate_initial_board()
        return True