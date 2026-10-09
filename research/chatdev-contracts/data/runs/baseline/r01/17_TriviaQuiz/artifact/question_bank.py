'''
question_bank.py
Provides the QuestionBank class, which loads, stores, filters and serves
quiz questions from configurable JSON or CSV question-bank files.
'''
import csv
import json
import os
import random
from questions import MultipleChoiceQuestion, ShortAnswerQuestion, Question
class QuestionBankError(Exception):
    """Raised when a question-bank file cannot be read or parsed."""
class QuestionBank:
    """Loads and manages a collection of Question objects."""
    SUPPORTED_EXTENSIONS = (".json", ".csv")
    def __init__(self):
        """Initialize an empty question bank."""
        self._questions = []
    def __len__(self):
        return len(self._questions)
    @property
    def questions(self):
        """Return a shallow copy of the bank's question list."""
        return list(self._questions)
    def add_question(self, question):
        """Append a Question instance to the bank after type-checking it."""
        if not isinstance(question, Question):
            raise TypeError("add_question expects a Question instance.")
        self._questions.append(question)
    def get_topics(self):
        """Return a sorted list of the distinct topics in the bank."""
        return sorted({q.topic for q in self._questions})
    def get_questions(self, topic=None, limit=None, shuffle=True, rng=None):
        """Return questions, optionally filtered by topic, limited and shuffled.
        Raises ValueError if limit is not a non-negative integer or None.
        """
        pool = self._questions
        if topic:
            wanted = topic.strip().lower()
            pool = [q for q in pool if q.topic.lower() == wanted]
        pool = list(pool)
        if limit is not None:
            try:
                limit = int(limit)
            except (TypeError, ValueError):
                raise ValueError("limit must be an integer or None, got %r" % (limit,))
            if limit < 0:
                raise ValueError("limit must be non-negative, got %d" % limit)
            pool = pool[:limit]
        if shuffle:
            (rng or random).shuffle(pool)
        return pool
    ...