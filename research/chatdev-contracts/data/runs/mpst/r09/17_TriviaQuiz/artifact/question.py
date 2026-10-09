'''
question.py
Defines the Question model for the ChatDev Trivia Quiz.
A Question is either MULTIPLE_CHOICE (lettered choices A-J) or SHORT_ANSWER
(free text with one or more accepted answers). It knows how to:
  * display()                -> render itself for the console
  * is_correct(input)        -> grade a user's answer (letter or text accepted)
  * correct_answer_display() -> readable correct answer for feedback/review
Grading is case-insensitive and ignores surrounding punctuation/whitespace.
'''
class Question:
    """A single trivia question with self-contained grading logic."""
    MULTIPLE_CHOICE = "multiple_choice"
    SHORT_ANSWER = "short_answer"
    LETTERS = "ABCDEFGHIJ"
    def __init__(self, text, question_type, answer, choices=None, topic="General"):
        """Validate and normalise all question data at construction time."""
        if not str(text).strip():
            raise ValueError("Question text must not be empty.")
        if question_type not in (self.MULTIPLE_CHOICE, self.SHORT_ANSWER):
            raise ValueError(
                f"Unknown question type '{question_type}'. Expected "
                f"'{self.MULTIPLE_CHOICE}' or '{self.SHORT_ANSWER}'."
            )
        self.text = str(text).strip()
        self.question_type = question_type
        self.topic = str(topic).strip() or "General"
        # ---------- choices (multiple choice only) ----------
        if question_type == self.MULTIPLE_CHOICE:
            if not isinstance(choices, (list, tuple)) or len(choices) < 2:
                raise ValueError(
                    "Multiple-choice questions require a 'choices' list "
                    "with at least 2 options."
                )
            self.choices = [str(c).strip() for c in choices if str(c).strip()]
            if len(self.choices) < 2:
                raise ValueError(
                    "Multiple-choice questions need at least 2 non-empty choices."
                )
            if len(self.choices) > len(self.LETTERS):
                raise ValueError(
                    f"At most {len(self.LETTERS)} choices are supported."
                )
            normalized = [self.normalize(c) for c in self.choices]
            if len(set(normalized)) != len(self.choices):
                raise ValueError("Multiple-choice options must be distinct.")
        else:
            self.choices = []
        # ---------- accepted answers ----------
        if isinstance(answer, (list, tuple)):
            answers = [str(a) for a in answer]
        else:
            answers = [str(answer)]
        answers = [a for a in answers if str(a).strip()]
        if not answers:
            raise ValueError("Question must have at least one correct answer.")
        if question_type == self.MULTIPLE_CHOICE:
            # Allow the answer to be given as a choice letter (e.g. "B")
            # and normalize it to the full choice text.
            resolved = []
            for ans in answers:
                token = ans.strip().rstrip(").").strip()
                if len(token) == 1 and token.upper() in self.LETTERS[: len(self.choices)]:
                    resolved.append(self.choices[self.LETTERS.index(token.upper())])
                else:
                    resolved.append(ans.strip())
            answers = resolved
        self.answers = answers
    # ---------- grading helpers ----------
    @staticmethod
    def normalize(value):
        """Lowercase, collapse whitespace, and strip trailing punctuation so
        answers compare forgivingly ('Paris.' == 'paris')."""
        text = " ".join(str(value).strip().lower().split())
        return text.rstrip(" .!?").strip()
    def letter_for_choice(self, user_input):
        """Return the uppercase choice letter if user_input names a valid
        choice letter (e.g. 'B' or 'b)'), otherwise None."""
        token = str(user_input).strip().rstrip(").").strip()
        if len(token) == 1 and token.upper() in self.LETTERS[: len(self.choices)]:
            return token.upper()
        return None
    # ---------- presentation ----------
    def display(self):
        """Render the question text; append lettered choices for MC."""
        lines = [self.text]
        if self.question_type == self.MULTIPLE_CHOICE:
            for i, choice in enumerate(self.choices):
                lines.append(f"   {self.LETTERS[i]}) {choice}")
        return "\n".join(lines)
    def correct_answer_display(self):
        """Human-readable string of the correct answer for feedback/review."""
        if self.question_type == self.MULTIPLE_CHOICE:
            for i, choice in enumerate(self.choices):
                if any(
                    self.normalize(choice) == self.normalize(ans)
                    for ans in self.answers
                ):
                    return f"{self.LETTERS[i]}) {choice}"
        return "; ".join(self.answers)  # show ALL accepted answers, not just [0]
    # ---------- grading ----------
    def is_correct(self, user_input):
        """Grade the user's answer against the accepted answers."""
        if user_input is None:
            return False
        if self.question_type == self.MULTIPLE_CHOICE:
            letter = self.letter_for_choice(user_input)
            if letter is not None:
                chosen = self.choices[self.LETTERS.index(letter)]
            else:
                chosen = user_input
            return any(
                self.normalize(chosen) == self.normalize(ans)
                for ans in self.answers
            )
        return any(
            self.normalize(user_input) == self.normalize(ans)
            for ans in self.answers
        )