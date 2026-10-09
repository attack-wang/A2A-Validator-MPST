def draw(self):
    canvas = self.canvas
    canvas.delete("all")
    # centre line
    canvas.create_rectangle(...)
    for paddle in self.paddles:
        paddle.draw(canvas)
    if self.state != "gameover":
        self.ball.draw(canvas)
    self.scoreboard.draw(canvas)
    if self.state == "serve":
        self._draw_message(...)
    elif self.state == "gameover":
        ...