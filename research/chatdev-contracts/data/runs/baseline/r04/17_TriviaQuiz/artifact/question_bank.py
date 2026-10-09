'''
question_bank.py
Loading, saving, and managing collections of quiz questions.
Class:
    QuestionBank -- holds questions and supports JSON/CSV import & export
'''
import csv
import json
import os
from question import MultipleChoiceQuestion, Question, ShortAnswerQuestion
class QuestionBank:
    """A configurable collection of trivia questions."""
    def __init__(self, questions=None):
        """Initialize the bank, optionally pre-loaded with Question objects."""
        self.questions = list(questions) if questions else []
    def __len__(self):
        return len(self.questions)
    def add_question(self, question):
        """Add a single Question instance to the bank."""
        if isinstance(question, Question):
            self.questions.append(question)
    def topics(self):
        """Return a sorted list of the unique topics present in the bank."""
        return sorted({question.topic for question in self.questions})
    def get_questions(self, topic=None, count=None, shuffle=False):
        """
        Return questions, optionally filtered by topic, limited in count,
        and/or shuffled.
        """
        import random
        selected = list(self.questions)
        if topic:
            wanted = str(topic).strip().lower()
            selected = [q for q in selected if q.topic.strip().lower() == wanted]
        if shuffle:
            random.shuffle(selected)
        if count is not None:
            selected = selected[:max(0, int(count))]
        return selected
    @staticmethod
    def _build_question(record):
        """Convert a raw dictionary record into the proper Question subclass."""
        q_type = str(record.get("type", "short_answer")).strip().lower()
        text = record.get("text", "")
        topic = record.get("topic", "General")
        answers = record.get("answers", record.get("answer", ""))
        if q_type in ("multiple_choice", "multiple-choice", "mc"):
            choices = record.get("choices", [])
            return MultipleChoiceQuestion(text, choices, answers, topic)
        return ShortAnswerQuestion(text, answers, topic)
    def load_from_json(self, filepath):
        """Load questions from a JSON file; returns the number loaded."""
        with open(filepath, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        if isinstance(data, dict):
            records = data.get("questions", [])
        elif isinstance(data, list):
            records = data
        else:
            records = []
        loaded = 0
        for record in records:
            if not isinstance(record, dict):
                continue  # Skip malformed (non-dict) records safely.
            try:
                self.add_question(self._build_question(record))
                loaded += 1
            except (TypeError, ValueError, AttributeError):
                continue
        return loaded
    def load_from_csv(self, filepath):
        """
        Load questions from a CSV file with the header:
        type,text,choices,answers,topic
        Choices and answers use '|' as the separator inside the cell.
        """
        loaded = 0
        with open(filepath, "r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                choices = [c for c in str(row.get("choices", "")).split("|") if c.strip()]
                answers = [a for a in str(row.get("answers", "")).split("|") if a.strip()]
                record = {
                    "type": row.get("type", "short_answer"),
                    "text": row.get("text", ""),
                    "choices": choices,
                    "answers": answers if answers else row.get("answers", ""),
                    "topic": row.get("topic", "General"),
                }
                self.add_question(self._build_question(record))
                loaded += 1
        return loaded
    def save_to_json(self, filepath):
        """Persist the current bank back to a JSON file."""
        records = []
        for question in self.questions:
            record = {
                "type": "multiple_choice" if isinstance(question, MultipleChoiceQuestion) else "short_answer",
                "topic": question.topic,
                "text": question.text,
                "answers": question.answers,
            }
            if isinstance(question, MultipleChoiceQuestion):
                record["choices"] = question.choices
            records.append(record)
        with open(filepath, "w", encoding="utf-8") as handle:
            json.dump({"questions": records}, handle, indent=2)
        return len(records)