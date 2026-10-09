'''
question.py
Defines the Question data model used by the trivia quiz program.
A Question can be either:
  * MultipleChoiceQuestion - offers a list of choices; the user may answer
    with the choice letter (A/B/C/D...), the choice number (1/2/3/4...) or
    the full text of the choice.
  * ShortAnswerQuestion    - the user types a free-form answer which is
    compared (case-insensitively, whitespace-trimmed) against the correct
    answer and any additional acceptable variants.
Both classes also know how to serialise themselves to / from plain
dictionaries so that question banks can be stored in JSON files.
'''
def normalize_text(value):
    """Lowercase, trim and collapse whitespace for tolerant answer comparison."""
    return " ".join(str(value).strip().lower().split())
class Question:
    """Base class for all quiz questions."""
    TYPE_NAME = "question"
    def __init__(self, text, topic="General", explanation=""):
        self.text = str(text)
        self.topic = str(topic)
        self.explanation = str(explanation or "")
    # ------------------------------------------------------------------ #
    # Abstract interface
    # ------------------------------------------------------------------ #
    def check_answer(self, answer):
        """Return True if the given user answer is correct."""
        raise NotImplementedError("Subclasses must implement check_answer().")
    def correct_answer_text(self):
        """Return a human-readable string of the correct answer."""
        raise NotImplementedError("Subclasses must implement correct_answer_text().")
    def to_dict(self):
        """Serialise this question to a plain dictionary (JSON-ready)."""
        raise NotImplementedError("Subclasses must implement to_dict().")
    # ------------------------------------------------------------------ #
    # Shared helpers
    # ------------------------------------------------------------------ #
    def format_for_display(self):
        """Return the question text as shown to the user during the quiz."""
        return f"[{self.topic}] {self.text}"
    @staticmethod
    def from_dict(data):
        """Build the concrete Question subclass matching `data["type"]`."""
        qtype = str(data.get("type", "short_answer")).strip().lower()
        # Imported lazily to avoid a circular import between the base and
        # the subclasses (the subclasses import this module).
        if qtype in ("multiple_choice", "mc", "choice"):
            from multiplechoicequestion import MultipleChoiceQuestion
            return MultipleChoiceQuestion.from_dict(data)
        from shortanswerquestion import ShortAnswerQuestion
        return ShortAnswerQuestion.from_dict(data)