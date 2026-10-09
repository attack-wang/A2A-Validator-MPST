'''
question_bank.py
Defines the QuestionBank class, which loads, stores, filters, and serves
trivia questions from configurable JSON question-bank files.
'''
import json
import os
import random
from question import Question
class QuestionBank:
    """Loads and manages a collection of trivia questions from a JSON file."""
    def __init__(self, name="Question Bank"):
        self.name = name
        self.questions = []
        self.source_file = None
    def add_question(self, question):
        """Append a Question instance to the bank."""
        if isinstance(question, Question):
            self.questions.append(question)
    def load_from_file(self, filepath):
        """
        Load questions from a JSON question-bank file.
        ...
        """
        ...