'''
question_bank.py
Loads and manages collections of trivia questions from configurable
JSON question-bank files.
Classes:
    QuestionBankError -- raised when a bank file is missing or malformed
    QuestionBank      -- loads questions and serves filtered/shuffled sets
'''
import glob
import json
import os
import random
from questions import MultipleChoiceQuestion, ShortAnswerQuestion
class QuestionBankError(Exception):
    """Raised when a question bank cannot be loaded or parsed."""
class QuestionBank:
    """Loads trivia questions from JSON files and serves them to the quiz."""
    def __init__(self, name="Untitled Bank"):
        self.name = name
        self.questions = []
        self.source_files = []
    def __len__(self):
        return len(self.questions)
    def add_question(self, question):
        """Append an already-built Question object to the bank."""
        self.questions.append(question)
    def load_from_json(self, filepath):
        """Load every question from a JSON question-bank file.
        The file may contain a documentation header before the JSON
        object; everything outside the outermost braces is ignored.
        Returns the number of questions loaded from the file.
        """
        if not os.path.isfile(filepath):
            raise QuestionBankError("Question bank file not found: {}".format(filepath))
        try:
            with open(filepath, "r", encoding="utf-8") as handle:
                raw_text = handle.read()
        except (OSError, UnicodeDecodeError) as error:
            raise QuestionBankError("Could not read {}: {}".format(filepath, error))
        data = self._parse_json_text(raw_text, filepath)
        loaded_before = len(self.questions)
        self.load_from_dict(data)
        self.source_files.append(filepath)
        return len(self.questions) - loaded_before
    def load_directory(self, directory):
        """Load every *.json file found in a directory. Returns file count."""
        pattern = os.path.join(directory, "*.json")
        files = sorted(glob.glob(pattern))
        if not files:
            raise QuestionBankError("No .json question banks found in: {}".format(directory))
        for filepath in files:
            self.load_from_json(filepath)
        return len(files)
    def load_from_dict(self, data):
        """Populate the bank from a dictionary following the bank schema."""
        if not isinstance(data, dict):
            raise QuestionBankError("Question bank must be a JSON object.")
        raw_questions = data.get("questions")
        if not isinstance(raw_questions, list) or not raw_questions:
            raise QuestionBankError("Question bank needs a non-empty 'questions' list.")
        if data.get("name"):
            self.name = str(data["name"])
        for position, item in enumerate(raw_questions, start=1):
            try:
                self.questions.append(self._build_question(item))
            except QuestionBankError as error:
                raise QuestionBankError("Question #{}: {}".format(position, error))
    @staticmethod
    def _parse_json_text(raw_text, filepath):
        """Parse JSON text, tolerating documentation around the JSON object."""
        text = raw_text.strip()
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass
        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end <= start:
            raise QuestionBankError("Invalid JSON in {}: no JSON object found".format(filepath))
        try:
            return json.loads(text[start:end + 1])
        except json.JSONDecodeError as error:
            raise QuestionBankError("Invalid JSON in {}: {}".format(filepath, error))
    @staticmethod
    def _build_question(item):
        """Convert one raw JSON entry into the proper Question object."""
        if not isinstance(item, dict):
            raise QuestionBankError("each question must be a JSON object")
        text = item.get("question")
        answer = item.get("answer")
        if not text or not str(text).strip():
            raise QuestionBankError("missing required 'question' text")
        if answer is None or (isinstance(answer, str) and not answer.strip()):
            raise QuestionBankError("missing required 'answer' field")
        topic = item.get("topic", "General")
        qtype = str(item.get("type", "short_answer")).strip().lower().replace("-", "_").replace(" ", "_")
        if qtype in ("multiple_choice", "mc", "choice"):
            choices = item.get("choices")
            if not isinstance(choices, list) or len(choices) < 2:
                raise QuestionBankError("multiple-choice questions need a 'choices' list with at least 2 options")
            if len(choices) > len(MultipleChoiceQuestion.LETTERS):
                raise QuestionBankError("too many choices (maximum {})".format(len(MultipleChoiceQuestion.LETTERS)))
            return MultipleChoiceQuestion(text, choices, answer, topic)
        if qtype in ("short_answer", "sa", "text", "fill_in"):
            alternatives = item.get("alternatives", [])
            if not isinstance(alternatives, list):
                raise QuestionBankError("'alternatives' must be a list of strings")
            return ShortAnswerQuestion(text, answer, topic, alternatives)
        raise QuestionBankError("unknown question type '{}' (use 'multiple_choice' or 'short_answer')".format(qtype))
    def get_topics(self):
        """Return a sorted list of the topics present in the bank."""
        return sorted({question.topic for question in self.questions})
    def get_questions(self, topic=None, count=None, shuffle=False):
        """Return questions, optionally filtered, shuffled, and limited."""
        selected = list(self.questions)
        if topic and str(topic).lower() not in ("all", ""):
            wanted = str(topic).lower()
            selected = [q for q in selected if q.topic.lower() == wanted]
        if shuffle:
            random.shuffle(selected)
        if count is not None:
            selected = selected[:max(0, int(count))]
        return selected
    def summary(self):
        """Return a short human-readable summary of the bank contents."""
        topics = self.get_topics()
        multiple = sum(1 for q in self.questions if q.question_type == "multiple_choice")
        short = len(self.questions) - multiple
        lines = [
            "Bank   : {}".format(self.name),
            "Files  : {}".format(", ".join(self.source_files) if self.source_files else "(none)"),
            "Total  : {} questions ({} multiple-choice, {} short-answer)".format(len(self), multiple, short),
            "Topics : {}".format(", ".join(topics) if topics else "(none)"),
        ]
        return "\n".join(lines)