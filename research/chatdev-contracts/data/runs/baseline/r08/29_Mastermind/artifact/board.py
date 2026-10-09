class Board:
    def __init__(self, code_length, max_attempts, color_count, use_color=None):
        self.code_length = code_length
        self.max_attempts = max_attempts
        self.color_count = color_count
        self.use_color = use_color if use_color is not None else True
        self.entries = []