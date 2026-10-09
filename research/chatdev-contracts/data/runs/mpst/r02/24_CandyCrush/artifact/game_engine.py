    def set_message(self, text, duration=2.5):
        """Set a transient HUD message shown by the GUI."""
        self.message = text
        self.message_timer = duration