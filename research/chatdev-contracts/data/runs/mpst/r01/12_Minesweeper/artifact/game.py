        if hit_mine:
            mine_cell = next((c for c in revealed if c.is_mine), cell)
            self.lost_cell = (mine_cell.row, mine_cell.col)
            self._lose()