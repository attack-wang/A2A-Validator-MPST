'''Loading, saving, and selecting questions from a question bank.'''
import json
import random
from question import MultipleChoiceQuestion, ShortAnswerQuestion, Question
class QuestionBank:
    '''Holds quiz questions and supports loading/saving JSON banks.'''
    def __init__(self, questions=None):
        '''Initialize the bank with an optional list of Question objects.'''
        self.questions = list(questions) if questions else []
    def add_question(self, question):
        '''Append a Question instance to the bank.'''
        self.questions.append(question)
    def topics(self):
        '''Return the sorted list of distinct topics present in the bank.'''
        return sorted({question.topic for question in self.questions})
    def select(self, topic=None, count=0, shuffle=True):
        '''Return the questions to play, filtered/limited/shuffled as requested.
        topic: keep only questions whose topic matches (None or "all" = keep all).
        count: maximum number of questions (0 = no limit).
        shuffle: randomize question order when True.
        '''
        if topic and topic != "all":
            selected = [q for q in self.questions if q.topic.lower() == topic.lower()]
        else:
            selected = list(self.questions)
        if shuffle:
            random.shuffle(selected)
        if count and count > 0:
            selected = selected[:count]
        return selected
    @classmethod
    def load(cls, path):
        '''Load a question bank from a JSON file, skipping malformed entries.'''
        bank = cls()
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        entries = data.get("questions", []) if isinstance(data, dict) else data
        if not isinstance(entries, list):
            raise ValueError("Question bank must contain a 'questions' list.")
        for entry in entries:
            question = cls._question_from_dict(entry)
            if question is not None:
                bank.add_question(question)
        return bank
    @staticmethod
    def _question_from_dict(entry):
        '''Convert one JSON entry into a Question, or None if it is invalid.'''
        if not isinstance(entry, dict):
            print("Warning: skipped non-object question entry.")
            return None
        q_type = str(entry.get("type", "short_answer")).strip().lower()
        text = entry.get("question")
        answer = entry.get("answer")
        topic = str(entry.get("topic", "General"))
        points = entry.get("points", 1)
        try:
            points = int(points)
        except (TypeError, ValueError):
            print("Warning: bad points value; defaulting to 1.")
            points = 1
        if not text or answer is None:
            print("Warning: skipped question missing text or answer.")
            return None
        try:
            if q_type in ("multiple_choice", "mc"):
                choices = entry.get("choices")
                if not isinstance(choices, list) or not choices:
                    print("Warning: skipped multiple-choice question without choices.")
                    return None
                return MultipleChoiceQuestion(text, choices, answer, topic, points)
            alternatives = entry.get("alternatives")
            if alternatives is not None and not isinstance(alternatives, list):
                alternatives = [alternatives]
            return ShortAnswerQuestion(text, answer, alternatives, topic, points)
        except ValueError as error:
            print("Warning: skipped invalid question ({}).".format(error))
            return None
    def save(self, path):
        '''Write the bank back to a JSON file so users can customize it.'''
        payload = {"questions": []}
        for question in self.questions:
            entry = {
                "topic": question.topic,
                "question": question.text,
                "answer": question.answer,
                "points": question.points,
            }
            if isinstance(question, MultipleChoiceQuestion):
                entry["type"] = "multiple_choice"
                entry["choices"] = question.choices
            else:
                entry["type"] = "short_answer"
                if question.alternatives:
                    entry["alternatives"] = question.alternatives
            payload["questions"].append(entry)
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, ensure_ascii=False)