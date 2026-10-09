def _update_reeling(self, game):
    self.length -= self._reel_speed()
    tx, ty = self.tip_position()
    if self.cargo is not None:
        self.cargo.x, self.cargo.y = tx, ty
    if self.length <= settings.CLAW_MIN_LENGTH:
        if self.cargo is not None:
            game.collect(self.cargo)
        self.reset()