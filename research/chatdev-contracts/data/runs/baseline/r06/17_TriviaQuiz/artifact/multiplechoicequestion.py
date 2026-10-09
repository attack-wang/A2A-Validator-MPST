'''
multiplechoicequestion.py
Concrete Question subclass for multiple-choice items. The stored answer may
be given as a letter (A/B/C...), a 1-based index or the full choice text;
it is resolved once at load time into an internal index. User answers are
accepted in any of the same three forms.
Fixes applied after testing:
  * `Question` and `normalize_text` are now imported from question.py
    (the class previously inherited from an unimported name).
  * `_resolve_answer_index` was completed (the previous version was
    truncated mid-statement and could not run).
'''
from question import Question, normalize_text
class MultipleChoiceQuestion(Question):
    """A question that offers a fixed list of choices to pick from."""
    TYPE_NAME = "multiple_choice"
    LETTERS = "ABCDEFGH"
    def __init__(self, text, choices, answer, topic="General", explanation=""):
        super().__init__(text, topic, explanation)
        if not choices or len(choices) < 2:
            raise ValueError("A multiple-choice question needs at least two choices.")
        if len(choices) > len(self.LETTERS):
            raise ValueError(f"At most {len(self.LETTERS)} choices are supported.")
        self.choices = [str(c) for c in choices]
        # The answer may be a letter, a 1-based index or the choice text;
        # resolve it once into an internal 0-based index.
        self._answer_index = self._resolve_answer_index(answer)
    def _resolve_answer_index(self, answer):
        """Turn a letter ('A'..), 1-based index or choice text into a 0-based index."""
        if isinstance(answer, bool):
            raise ValueError("Answer must be a letter, an index or the choice text.")
        if isinstance(answer, int):
            index = answer - 1
            if not 0 <= index < len(self.choices):
                raise ValueError(
                    f"Answer index {answer} is out of range 1..{len(self.choices)}."
                )
            return index
        text = normalize_text(answer)
        if not text:
            raise ValueError("Answer must be a letter, an index or the choice text.")
        letters = self.LETTERS[:len(self.choices)]
        if len(text) == 1 and text.upper() in letters:
            return letters.index(text.upper())
        if text.isdigit():
            index = int(text) - 1
            if not 0 <= index < len(self.choices):
                raise ValueError(
                    f"Answer index {text} is out of range 1..{len(self.choices)}."
                )
            return index
        for position, choice in enumerate(self.choices):
            if normalize_text(choice) == text:
                return position
        raise ValueError(f"Answer '{answer}' does not match any choice.")
    def check_answer(self, answer):
        """Accept a letter, 1-based number or the full choice text."""
        if answer is None:
            return False
        text = str(answer).strip()
        if not text:
            return False
        letters = self.LETTERS[:len(self.choices)]
        if len(text) == 1 and text.upper() in letters:
            return letters.index(text.upper()) == self._answer_index
        if text.isdigit():
            return int(text) - 1 == self._answer_index
        return normalize_text(text) == normalize_text(self.choices[self._answer_index])
    def correct_answer_text(self):
        letter = self.LETTERS[self._answer_index]
        return f"{letter}. {self.choices[self._answer_index]}"
    def format_for_display(self):
        lines = [super().format_for_display()]
        for position, choice in enumerate(self.choices):
            lines.append(f"  {self.LETTERS[position]}. {choice}")
        return "\n".join(lines)
    def to_dict(self):
        data = {
            "type": self.TYPE_NAME,
            "topic": self.topic,
            "question": self.text,
            "choices": list(self.choices),
            "answer": self.choices[self._answer_index],
        }
        if self.explanation:
            data["explanation"] = self.explanation
        return data
    @classmethod
    def from_dict(cls, data):
        return cls(
            text=data.get("question", ""),
            choices=data.get("choices") or [],
            answer=data.get("answer", ""),
            topic=data.get("topic", "General") or "General",
            explanation=data.get("explanation", "") or "",
        )