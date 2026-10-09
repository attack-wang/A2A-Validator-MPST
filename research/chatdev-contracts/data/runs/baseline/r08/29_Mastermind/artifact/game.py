class Game:
    '''One round of Mastermind from code generation to win/lose outcome.'''
    def __init__(self, settings, board, input_func=input, output_func=print):
        self.settings = settings
        self.board = board
        self._input = input_func
        self._output = output_func
        self.secret_code = generate_secret_code(
            code_length=settings["code_length"],
            color_count=settings["color_count"],
            allow_duplicates=settings["allow_duplicates"],
        )
        self.code_length = settings["code_length"]
        self.max_attempts = settings["max_attempts"]
        self.attempts_used = 0
        self.won = False
        self.finished = False
        self.abandoned = False
    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def play(self):
        '''Run the round until the player wins, loses, or quits.'''
        self._print_welcome()
        while not self.finished:
            self._render_board()
            guess = self._prompt_guess()
            if guess is None:
                break  # player quit or input stream closed
            self._process_guess(guess)
        if self.finished:
            self._print_outcome()
        elif self.abandoned:
            self._print_abandoned()
    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _print_welcome(self):
        self._output("")
        self._output("A secret code of {0} colors has been hidden. You have {1} attempts.".format(
            self.code_length, self.max_attempts))
        palette = list(COLORS.items())[:self.settings["color_count"]]
        self._output("Palette: " + ", ".join("{0}={1}".format(k, v["name"]) for k, v in palette))
        self._output("Feedback legend: EXACT = right color & position, PARTIAL = right color, wrong position.")
        self._output("Type 'h' for help, 'r' for rules, 'q' to quit.")
    def _render_board(self):
        self._output("")
        self._output(self.board.render())
    def _prompt_guess(self):
        '''Ask for a guess; returns a validated guess list, or None to quit.'''
        prompt = "Attempt {0}/{1} — enter your guess (e.g. {2}) or 'h'/'r'/'q': ".format(
            self.attempts_used + 1, self.max_attempts,
            "1234"[:self.code_length])
        while True:
            try:
                raw = self._input(prompt)
            except (EOFError, KeyboardInterrupt):
                self.abandoned = True
                return None
            command = raw.strip().lower()
            if command in ("h", "help"):
                self._print_help()
                continue
            if command in ("r", "rules"):
                self._print_rules()
                continue
            if command in ("q", "quit", "exit"):
                self.abandoned = True
                return None
            guess, error = normalize_guess(raw, self.code_length)
            if error is not None:
                self._output("  ✗ {0}".format(error))
                continue
            return guess
    def _process_guess(self, guess):
        '''Evaluate the guess, update the board and the round state.'''
        feedback = evaluate_guess(self.secret_code, guess)
        self.board.add_entry(guess, feedback)
        self.attempts_used += 1
        if feedback.exact == self.code_length:
            self.won = True
            self.finished = True
        elif self.attempts_used >= self.max_attempts:
            self.won = False
            self.finished = True
        else:
            self._output("  Feedback: {0} exact, {1} partial.".format(feedback.exact, feedback.partial))
    def _print_outcome(self):
        self._output("")
        self._output(self.board.render_outcome(
            won=self.won,
            secret_code=self.secret_code,
            attempts_used=self.attempts_used,
            max_attempts=self.max_attempts,
        ))
    def _print_abandoned(self):
        self._output("")
        self._output("Round abandoned — the secret code was: {0}.".format(
            " ".join(self.secret_code)))
    def _print_help(self):
        self._output("  Help — enter {0} colors per guess.".format(self.code_length))
        self._output("  Digits 1-6 pick colors; letters R G B Y O P also work.")
        self._output("  Separators (spaces, commas) are ignored: '1 2 3 4' == '1234' == 'r,g,b,y'.")
        self._output("  Commands: 'h' = help, 'r' = rules, 'q' = quit the round.")
    def _print_rules(self):
        self._output("  Rules — the computer hides a code of {0} colors; you have {1} attempts.".format(
            self.code_length, self.max_attempts))
        self._output("  After each guess you learn how many pegs are EXACT (right color & position)")
        self._output("  and how many are PARTIAL (right color, wrong position).")
        self._output("  Crack the full code before you run out of attempts to win!")