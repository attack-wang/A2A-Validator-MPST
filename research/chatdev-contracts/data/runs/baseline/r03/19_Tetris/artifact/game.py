if not self.board.is_valid_position(self.current_piece, dy=1):
    self.lock_timer += dt
    if self.lock_timer >= LOCK_DELAY:
        self._lock_piece()
else:
    self.lock_timer = 0.0
    self.fall_timer += dt
    if self.fall_timer >= self.drop_interval:
        self.fall_timer = 0.0
        self.current_piece.move(0, 1)