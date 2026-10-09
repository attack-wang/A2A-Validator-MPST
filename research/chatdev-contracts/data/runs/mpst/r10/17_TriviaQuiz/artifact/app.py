'''
app.py
Interactive console front-end for the trivia quiz program.
Provides:
    QuizApp -- menu-driven application that lets the user pick a question
               bank, configure quiz options, play, and review results
'''
import glob
import os
import sys
from question_bank import QuestionBank, QuestionBankError
from quiz import Quiz
class QuizApp:
    """Menu-driven console application that runs trivia quizzes."""
    def __init__(self, bank_directory="question_banks"):
        self.bank_directory = bank_directory
        self.bank = None
        self.settings = {
            "shuffle": True,
            "question_count": None,   # None = use all questions
            "topic": "all",
            "show_answers_at_end": True,
        }
    # ---------- helpers ----------
    @staticmethod
    def prompt(message, valid=None, default=None, allow_blank=False):
        ...
    def discover_bank_files(self):
        """Find JSON question-bank files in the bank directory."""
        pattern = os.path.join(self.bank_directory, "*.json")
        files = sorted(glob.glob(pattern))
        if not files:
            # fall back to current directory
            files = sorted(glob.glob("*.json"))
        return files
    def choose_question_bank(self):
        ...
    def configure_settings(self):
        ...
    def run_quiz(self):
        ...
    def run(self):
        ...