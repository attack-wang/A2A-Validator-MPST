def _capture_chains(self, current, path, captured, out):
    piece = self.get_piece(current.row, current.col)
    extended = False
    for dr, dc in self._capture_directions(piece):
        mid = Position(current.row + dr, current.col + dc)
        land = Position(current.row + 2 * dr, current.col + 2 * dc)
        if not self.in_bounds(land.row, land.col):
            continue
        victim = self.get_piece(mid.row, mid.col)
        if victim is None or victim.player is piece.player:
            continue
        if not self.is_empty(land.row, land.col) or land in captured:
            continue
        extended = True
        sim = self.copy()
        sim.grid[mid.row][mid.col] = None
        sim.grid[current.row][current.col] = None
        crowned = (not piece.is_king) and land.row == piece.player.promotion_row
        sim.grid[land.row][land.col] = Piece(piece.player, is_king=piece.is_king or crowned)
        new_path = path + [land]
        new_captured = captured + [mid]
        if crowned:
            out.append(Move(new_path, new_captured))
        else:
            sim._capture_chains(land, new_path, new_captured, out)
    if not extended and captured:
        out.append(Move(list(path), list(captured)))