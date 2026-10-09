'''
questionbank.py
Loading, validation, and management of trivia question collections.
Classes:
    QuestionBank      - In-memory collection of questions with filtering.
    QuestionBankError - Raised when a question bank file or entry is invalid.
Functions:
    parse_question_entry(entry) - Converts one dict entry into a Question.
    build_default_bank()        - Returns a QuestionBank with built-in samples.
The expected JSON schema for a bank file is:
    {
      "questions": [
        {
          "type": "multiple_choice",
          "topic": "Geography",
          "question": "What is the capital of France?",
          "choices": ["London", "Paris", "Berlin", "Madrid"],
          "answer": "Paris",
          "explanation": "Paris has been France's capital since..."
        },
        {
          "type": "short_answer",
          "topic": "Science",
          "question": "Which planet is known as the Red Planet?",
          "answer": "Mars",
          "accepted_answers": ["Mars", "the red planet"],
          "explanation": "Iron oxide dust gives Mars its red colour."
        }
      ]
    }
'''
import json
import os
import random
from question import MultipleChoiceQuestion, ShortAnswerQuestion
class QuestionBankError(Exception):
    """Raised when a question bank file or one of its entries is invalid."""
def parse_question_entry(entry):
    """Convert one question dict into the appropriate Question instance.
    Raises QuestionBankError when the entry is not a dict, is missing
    required fields, has an unknown type, or contains invalid data.
    """
    if not isinstance(entry, dict):
        raise QuestionBankError("Entry must be a JSON object (dict).")
    entry_type = str(entry.get("type", "")).strip().lower()
    text = str(entry.get("question", "")).strip()
    topic = str(entry.get("topic", "General")).strip() or "General"
    explanation = str(entry.get("explanation", "")).strip()
    if not text:
        raise QuestionBankError("Missing required field 'question'.")
    if entry_type in ("multiple_choice", "multiplechoice", "mc"):
        choices = entry.get("choices")
        if not isinstance(choices, list):
            raise QuestionBankError(
                "'multiple_choice' questions need a 'choices' list."
            )
        choices = [str(choice).strip() for choice in choices if str(choice).strip()]
        if len(choices) < 2:
            raise QuestionBankError(
                "'multiple_choice' questions need at least 2 non-empty choices."
            )
        if len(choices) > len(MultipleChoiceQuestion.LETTERS):
            raise QuestionBankError(
                "Too many choices; the maximum is {}.".format(len(MultipleChoiceQuestion.LETTERS))
            )
        answer = entry.get("answer")
        if answer is None or not str(answer).strip():
            raise QuestionBankError("Missing required field 'answer'.")
        question = MultipleChoiceQuestion(text, choices, str(answer).strip(), topic, explanation)
        if question._answer_index() is None:
            raise QuestionBankError(
                "Answer '{}' does not match any choice, letter, or number.".format(answer)
            )
        return question
    if entry_type in ("short_answer", "shortanswer", "sa"):
        answer = entry.get("answer")
        if answer is None or not str(answer).strip():
            raise QuestionBankError("Missing required field 'answer'.")
        accepted = entry.get("accepted_answers")
        if accepted is not None and not isinstance(accepted, list):
            raise QuestionBankError("'accepted_answers' must be a list of strings.")
        return ShortAnswerQuestion(text, str(answer).strip(), topic, explanation, accepted)
    raise QuestionBankError(
        "Unknown question type '{}': expected 'multiple_choice' or 'short_answer'.".format(
            entry_type or "<missing>"
        )
    )
class QuestionBank:
    """An in-memory collection of trivia questions."""
    def __init__(self, questions=None):
        """Create a bank, optionally seeded with an initial question list."""
        self.questions = list(questions) if questions else []
    def __len__(self):
        """Return the number of questions held by the bank."""
        return len(self.questions)
    def add_question(self, question):
        """Append a Question instance to the bank."""
        self.questions.append(question)
    def get_topics(self):
        """Return the sorted list of distinct topics in the bank."""
        return sorted({question.topic for question in self.questions})
    def get_questions(self, topic=None, count=None, shuffle=False):
        """Return questions filtered by topic, limited to `count`, optionally shuffled."""
        selected = self.questions
        if topic:
            selected = [q for q in selected if q.topic.lower() == topic.lower()]
        selected = list(selected)
        if shuffle:
            random.shuffle(selected)
        if count is not None:
            selected = selected[:max(0, int(count))]
        return selected
    @classmethod
    def load_from_json(cls, path):
        """Build a QuestionBank from a JSON file, raising QuestionBankError on problems."""
        if not os.path.isfile(path):
            raise QuestionBankError("Question bank file not found: {}".format(path))
        try:
            with open(path, "r", encoding="utf-8") as handle:
                data = json.load(handle)
        except json.JSONDecodeError as error:
            raise QuestionBankError("Could not parse JSON in '{}': {}".format(path, error))
        except OSError as error:
            raise QuestionBankError("Could not read '{}': {}".format(path, error))
        if not isinstance(data, dict) or not isinstance(data.get("questions"), list):
            raise QuestionBankError(
                "Invalid bank format in '{}': expected a JSON object with a 'questions' list.".format(path)
            )
        bank = cls()
        for position, entry in enumerate(data["questions"], start=1):
            try:
                bank.add_question(parse_question_entry(entry))
            except QuestionBankError as error:
                raise QuestionBankError("Question #{}: {}".format(position, error))
        if not bank.questions:
            raise QuestionBankError("The bank file '{}' contains no questions.".format(path))
        return bank
DEFAULT_QUESTIONS = [
    {
        "type": "multiple_choice",
        "topic": "Geography",
        "question": "What is the capital of France?",
        "choices": ["London", "Paris", "Berlin", "Madrid"],
        "answer": "Paris",
        "explanation": "Paris has been France's capital since the late 10th century.",
    },
    {
        "type": "multiple_choice",
        "topic": "Geography",
        "question": "Which river is traditionally considered the longest in the world?",
        "choices": ["Amazon", "Nile", "Yangtze", "Mississippi"],
        "answer": "Nile",
        "explanation": "The Nile runs about 6,650 km (the Amazon is a close second).",
    },
    {
        "type": "multiple_choice",
        "topic": "Science",
        "question": "What is the chemical symbol for gold?",
        "choices": ["Go", "Gd", "Au", "Ag"],
        "answer": "Au",
        "explanation": "Au comes from the Latin word 'aurum'.",
    },
    {
        "type": "short_answer",
        "topic": "Science",
        "question": "Which planet is known as the Red Planet?",
        "answer": "Mars",
        "accepted_answers": ["Mars", "the red planet"],
        "explanation": "Iron oxide dust gives Mars its red colour.",
    },
    {
        "type": "short_answer",
        "topic": "Science",
        "question": "What gas do plants primarily absorb for photosynthesis?",
        "answer": "Carbon dioxide",
        "accepted_answers": ["carbon dioxide", "co2"],
        "explanation": "Plants take in CO2 and release oxygen during photosynthesis.",
    },
    {
        "type": "multiple_choice",
        "topic": "History",
        "question": "In which year did World War II end?",
        "choices": ["1943", "1944", "1945", "1946"],
        "answer": "1945",
        "explanation": "WWII ended in 1945 (Germany surrendered in May, Japan in September).",
    },
    {
        "type": "short_answer",
        "topic": "History",
        "question": "Who was the first President of the United States?",
        "answer": "George Washington",
        "accepted_answers": ["George Washington", "Washington"],
        "explanation": "George Washington served from 1789 to 1797.",
    },
    {
        "type": "multiple_choice",
        "topic": "Literature",
        "question": "Who wrote the play 'Romeo and Juliet'?",
        "choices": ["Charles Dickens", "William Shakespeare", "Jane Austen", "Mark Twain"],
        "answer": "William Shakespeare",
        "explanation": "Shakespeare wrote the tragedy around 1594-1596.",
    },
    {
        "type": "short_answer",
        "topic": "General",
        "question": "How many sides does a hexagon have?",
        "answer": "6",
        "accepted_answers": ["6", "six"],
        "explanation": "A hexagon is a polygon with six sides.",
    },
    {
        "type": "multiple_choice",
        "topic": "General",
        "question": "What colour do you get when you mix blue and yellow paint?",
        "choices": ["Green", "Purple", "Orange", "Brown"],
        "answer": "Green",
        "explanation": "Blue and yellow pigments combine to make green.",
    },
]
def build_default_bank():
    """Return a QuestionBank pre-loaded with the built-in sample questions."""
    bank = QuestionBank()
    for entry in DEFAULT_QUESTIONS:
        bank.add_question(parse_question_entry(entry))
    return bank