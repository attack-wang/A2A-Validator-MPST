'''
questionbank.py
Loading and validation of question banks.
Defines:
- QuestionBank: a titled collection of questions loaded from a JSON file.
The JSON file must look like:
{
    "title": "My Quiz",
    "questions": [ ... ]   # see question.py docstring for the question format
}
'''
import json
from question import MultipleChoiceQuestion, ShortAnswerQuestion
class QuestionBank:
    """A titled collection of questions loaded from a JSON file."""
    VALID_TYPES = ("multiple_choice", "short_answer")
    def __init__(self, title="Trivia Quiz", questions=None):
        self.title = str(title).strip() or "Trivia Quiz"
        self.questions = list(questions) if questions else []
    def __len__(self):
        return len(self.questions)
    @classmethod
    def load_from_file(cls, path):
        """Load and validate a question bank from a JSON file."""
        with open(path, "r", encoding="utf-8") as handle:
            try:
                data = json.load(handle)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    "Question bank file '%s' is not valid JSON: %s" % (path, exc)
                ) from exc
        return cls.from_dict(data, source=path)
    @classmethod
    def from_dict(cls, data, source=""):
        """Build a QuestionBank from an already-parsed JSON dictionary."""
        prefix = "Question bank '%s': " % source if source else "Question bank: "
        if not isinstance(data, dict):
            raise ValueError(prefix + "top-level structure must be a JSON object.")
        title = data.get("title", "Trivia Quiz")
        raw_questions = data.get("questions")
        if not isinstance(raw_questions, list) or not raw_questions:
            raise ValueError(prefix + "must contain a non-empty 'questions' list.")
        questions = []
        for position, raw in enumerate(raw_questions, start=1):
            questions.append(cls._build_question(raw, position, prefix))
        return cls(title=title, questions=questions)
    @classmethod
    def _build_question(cls, raw, position, error_prefix):
        """Convert one raw JSON question object into a Question instance."""
        location = "%squestion #%d" % (error_prefix, position)
        if not isinstance(raw, dict):
            raise ValueError(location + " must be a JSON object.")
        qtype = (
            str(raw.get("type", "short_answer"))
            .strip()
            .lower()
            .replace(" ", "_")
            .replace("-", "_")
        )
        text = raw.get("question") or raw.get("text")
        topic = raw.get("topic", "General")
        answer = raw.get("answer")
        if not text:
            raise ValueError(location + " is missing its 'question' text.")
        if qtype in ("multiple_choice", "mc"):
            if "options" not in raw:
                raise ValueError(location + " (multiple choice) is missing 'options'.")
            if answer is None:
                raise ValueError(location + " (multiple choice) is missing 'answer'.")
            return MultipleChoiceQuestion(text, raw["options"], answer, topic)
        if qtype in ("short_answer", "short", "text"):
            if answer is None:
                raise ValueError(location + " (short answer) is missing 'answer'.")
            return ShortAnswerQuestion(text, answer, topic)
        raise ValueError(
            location + " has unknown type '%s'. Valid types: %s."
            % (raw.get("type"), ", ".join(cls.VALID_TYPES))
        )