class ConsoleUI:
    def __init__(self, game):
        self.game = game
        self.use_unicode = supports_unicode()
        self.use_color = sys.stdout.isatty()
        self.pegs = {
            "exact": "X" if not self.use_unicode else EXACT_PEG,
            ...
        }