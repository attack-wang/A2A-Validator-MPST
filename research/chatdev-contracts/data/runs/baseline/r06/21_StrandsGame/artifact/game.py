class StrandsGame:
    COMMANDS = {
        "merge": "_cmd_merge", "m": "_cmd_merge",
        "unmerge": "_cmd_unmerge", "u": "_cmd_unmerge",
        "hint": "_cmd_hint", "h": "_cmd_hint",
        "board": "_cmd_board", "b": "_cmd_board",
        "words": "_cmd_words", "w": "_cmd_words",
        "help": "_cmd_help", "?": "_cmd_help",
        "quit": "_cmd_quit", "q": "_cmd_quit",
    }
    def __init__(self, puzzle, ui=None, validator=None):
        self.puzzle = puzzle
        self.ui = ui or ConsoleUI()
        self.validator = validator or MergeValidator(puzzle.dictionary)
        self.stats = {"merges": 0, "hints": 0, "invalid": 0}
        self.hint_level = 0
        self.running = True
    def run(self):
        self.ui.show_welcome(...)
        self.ui.show_strands(self.puzzle)
        self.ui.show_help()
        while self.running:
            try:
                raw = self.ui.prompt()
            except (EOFError, KeyboardInterrupt):
                self._cmd_quit([])
                break
            if not raw.strip():
                continue
            self._handle_command(raw)
            self._check_completion()  # hmm, only after merge?