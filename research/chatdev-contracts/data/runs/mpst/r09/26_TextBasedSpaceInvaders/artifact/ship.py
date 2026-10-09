    def _bind_keys(self):
        self.root.bind("<KeyPress>", self._on_keydown)
        self.root.bind("<KeyRelease>", self._on_keyup)
    def _on_keydown(self, event):
        key = event.keysym.lower()
        if key == "escape":
            self._on_close()
            return
        if self.state == self.STATE_MENU:
            if key in ("return", "space"):
                self.reset_game()
                self.state = self.STATE_PLAYING
        elif self.state == self.STATE_PLAYING:
            if key == "p":
                self.state = self.STATE_PAUSED
            elif key == "space":
                self._fire()
            else:
                self.keys.add(key)
        elif self.state == self.STATE_PAUSED:
            if key == "p":
                self.state = self.STATE_PLAYING
        elif self.state in (self.STATE_GAME_OVER, self.STATE_VICTORY):
            if key in ("return", "space"):
                self.reset_game()
                self.state = self.STATE_PLAYING
    def _on_keyup(self, event):
        self.keys.discard(event.keysym.lower())