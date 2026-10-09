if self.ball.x + self.ball.radius < 0:
    self.score_right += 1
    self._after_point(-1)           # re-serve toward the player who missed (left)
elif self.ball.x - self.ball.radius > SCREEN_WIDTH:
    self.score_left += 1
    self._after_point(1)            # re-serve toward the player who missed (right)