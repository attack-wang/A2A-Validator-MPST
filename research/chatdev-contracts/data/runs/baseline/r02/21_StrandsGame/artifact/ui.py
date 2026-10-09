class UI:
    COLORS = {...}
    def __init__(self, use_color=True)
    def clear(self)
    def title(self)
    def render(self, state) -> str
    def render_strands(self, state): display available strands in a grid, 5 per row, each cell like "[1] CAT ", selected ones highlighted with different bracket style like "<1> CAT" or inverse video.
    def render_found(self, state): list found words with key target highlighted.
    def render_selection(self, state): current merge text like "CAT + ER + PIL = CATERPIL..."
    def render_log(self, state): last few messages.
    def help_text(self)
    def celebration(self, state)