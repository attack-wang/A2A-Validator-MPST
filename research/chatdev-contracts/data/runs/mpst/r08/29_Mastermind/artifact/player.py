class Player:
    def __init__(self, code_length, view):
        self.code_length = code_length
        self.view = view
    def _parse(self, raw):
        tokens = raw.replace(',', ' ').replace('-', ' ').split()
        codes = [token.upper() for token in tokens]
        if len(codes) == 1 and len(codes[0]) > 1:
            codes = list(codes[0])
        if len(codes) != self.code_length:
            self.view.show_length_error(self.code_length, len(codes))
            return None
        invalid = [c for c in codes if c not in config.AVAILABLE_COLORS]
        if invalid:
            self.view.show_invalid_colors(sorted(set(invalid)))
            return None
        return codes
    def get_guess(self, attempt, max_attempts):
        prompt = 'Attempt {}/{} - your guess: '.format(attempt, max_attempts)
        while True:
            raw = input(prompt).strip()
            if not raw:
                continue
            command = raw.lower()
            if command in ('quit', 'exit', 'q'):
                return None
            if command in ('help', 'h', '?'):
                self.view.show_help(self.code_length)
                continue
            codes = self._parse(raw)
            if codes is not None:
                return codes