'''
feedback_renderer.py
...
'''
class Feedback:
    CORRECT = "GREEN"
    PRESENT = "YELLOW"
    ABSENT = "GREY"
COLOR_MAP = {
    "GREEN": "\033[92m",
    "YELLOW": "\033[93m",
    "GREY": "\033[90m",
    "RESET": "\033[0m",
    "BOLD": "\033[1m",
}
class FeedbackRenderer:
    def __init__(self, use_color=True):
        self.use_color = use_color
    def _colorize(self, text, color):
        if not self.use_color:
            return text
        return f"{COLOR_MAP[color]}{text}{COLOR_MAP['RESET']}"
    def render_guess(self, guess, feedback):
        tiles = []
        for letter, state in zip(guess.upper(), feedback):
            tiles.append(self._colorize(f" {letter} ", state))
        return "|".join(tiles)  # or with brackets