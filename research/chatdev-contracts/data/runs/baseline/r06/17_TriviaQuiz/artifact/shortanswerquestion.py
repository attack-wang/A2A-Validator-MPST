'''
shortanswerquestion.py
Concrete Question subclass for free-form short-answer items. The user's
answer is compared case-insensitively against the stored answer and any
extra acceptable variants, after trimming and collapsing whitespace.
Fix applied after testing: `Question` and `normalize_text` are now imported
from question.py (previously referenced without an import, which raised a
NameError the first time a short-answer question was graded).
'''
from question import Question, normalize_text
class ShortAnswerQuestion(Question):
    """A question answered with free-form text."""
    TYPE_NAME = "short_answer"
    def __init__(self, text, answer, acceptable_answers=None, topic="General", explanation=""):
        super().__init__(text, topic, explanation)
        if answer is None or not str(answer).strip():
            raise ValueError("A short-answer question needs a non-empty answer.")
        self.answer = str(answer).strip()
        self.acceptable_answers = [str(a) for a in (acceptable_answers or [])]
    def check_answer(self, answer):
        if answer is None:
            return False
        guess = normalize_text(answer)
        if not guess:
            return False
        candidates = [normalize_text(self.answer)]
        candidates.extend(normalize_text(a) for a in self.acceptable_answers)
        return guess in candidates
    def correct_answer_text(self):
        return self.answer
    def to_dict(self):
        data = {
            "type": self.TYPE_NAME,
            "topic": self.topic,
            "question": self.text,
            "answer": self.answer,
        }
        if self.acceptable_answers:
            data["acceptable_answers"] = list(self.acceptable_answers)
        if self.explanation:
            data["explanation"] = self.explanation
        return data
    @classmethod
    def from_dict(cls, data):
        return cls(
            text=data.get("question", ""),
            answer=data.get("answer", ""),
            acceptable_answers=data.get("acceptable_answers") or [],
            topic=data.get("topic", "General") or "General",
            explanation=data.get("explanation", "") or "",
        )