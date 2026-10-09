'''
QuestionBank: loads and manages trivia questions from JSON question bank files.
A question bank file is a JSON document with the following structure:
    {
        "name": "General Knowledge",
        "questions": [
            {
                "type": "multiple_choice",
                "topic": "Geography",
                "text": "What is the capital of Australia?",
                "options": ["Sydney", "Melbourne", "Canberra", "Perth"],
                "answer": "Canberra",
                "explanation": "Canberra was purpose-built as the capital in 1913."
            },
            {
                "type": "short_answer",
                "topic": "Astronomy",
                "text": "Which planet is known as the Red Planet?",
                "answer": "Mars",
                "alternatives": ["the red planet"],
                "explanation": "Mars appears red due to iron oxide on its surface."
            }
        ]
    }
Recognized question types: "multiple_choice" (aliases: "multiple-choice", "mcq")
and "short_answer" (aliases: "short-answer", "short"). Questions missing the
"type" field default to "short_answer".
'''
import json
import os
import random
from questions import Question, MultipleChoiceQuestion, ShortAnswerQuestion
class QuestionBankError(Exception):
    '''Raised when a question bank file cannot be found, read, or parsed.'''
class QuestionBank:
    '''Loads trivia questions from a JSON question bank file and serves
    filtered/shuffled selections of those questions to the quiz engine.'''
    MCQ_TYPE_ALIASES = ("multiple_choice", "multiple-choice", "mcq")
    SHORT_TYPE_ALIASES = ("short_answer", "short-answer", "short")
    def __init__(self, name="Question Bank"):
        '''Initialize an empty question bank with a display name.'''
        self.name = name
        self.questions = []
    @classmethod
    def load(cls, filepath):
        '''Load a question bank from a JSON file.
        Returns a fully populated QuestionBank instance. Raises
        QuestionBankError if the file is missing, unreadable, invalid JSON,
        or contains malformed questions.
        '''
        if not os.path.exists(filepath):
            raise QuestionBankError(f"Question bank file not found: {filepath}")
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise QuestionBankError(f"Invalid JSON in {filepath}: {e}")
        except UnicodeDecodeError as e:
            raise QuestionBankError(f"Encoding error in {filepath}: {e}")
        except (OSError, IOError) as e:
            raise QuestionBankError(f"Could not read {filepath}: {e}")
        if not isinstance(data, dict):
            raise QuestionBankError(
                f"Invalid question bank format in {filepath}: top-level JSON must be an object")
        bank = cls(name=data.get("name", os.path.splitext(os.path.basename(filepath))[0]))
        raw_questions = data.get("questions", [])
        if not isinstance(raw_questions, list):
            raise QuestionBankError(
                f"Invalid question bank format in {filepath}: 'questions' must be a list")
        if not raw_questions:
            raise QuestionBankError(f"No questions found in {filepath}")
        for i, item in enumerate(raw_questions):
            try:
                bank.questions.append(cls._parse_question(item))
            except (KeyError, ValueError, TypeError) as e:
                raise QuestionBankError(f"Error in question #{i + 1} of {filepath}: {e}")
        return bank
    @staticmethod
    def _parse_question(item):
        '''Convert one raw JSON dict into the appropriate Question subclass.'''
        if not isinstance(item, dict):
            raise TypeError("each question must be a JSON object")
        text = item.get("text")
        answer = item.get("answer")
        if not isinstance(text, str) or not text.strip():
            raise ValueError("each question needs non-empty 'text'")
        if answer is None or (isinstance(answer, str) and not answer.strip()):
            raise ValueError("each question needs a non-empty 'answer'")
        qtype = str(item.get("type", "short_answer")).lower()
        common = dict(
            text=text,
            answer=answer,
            topic=item.get("topic", "General"),
            explanation=item.get("explanation"),
        )
        if qtype in QuestionBank.MCQ_TYPE_ALIASES:
            options = item.get("options")
            if not options or not isinstance(options, list) or len(options) < 2:
                raise ValueError("multiple choice questions need at least 2 options")
            return MultipleChoiceQuestion(options=options, **common)
        elif qtype in QuestionBank.SHORT_TYPE_ALIASES:
            alternatives = item.get("alternatives")
            if alternatives is not None and not isinstance(alternatives, list):
                alternatives = [alternatives]
            return ShortAnswerQuestion(alternatives=alternatives, **common)
        else:
            raise ValueError(f"unknown question type '{qtype}'")
    def get_topics(self):
        '''Return a sorted list of the distinct topics present in the bank.'''
        return sorted({q.topic for q in self.questions})
    def get_questions(self, topic=None, count=None, shuffle=True):
        '''Return questions from the bank.
        topic:  only questions whose topic matches (case-insensitive);
                None or "all" returns every question.
        count:  limit the result to at most this many questions.
        shuffle: randomize the order of the returned questions.
        '''
        pool = self.questions
        if topic and topic.lower() != "all":
            pool = [q for q in pool if q.topic.lower() == topic.lower()]
        if not pool:
            return []
        pool = list(pool)
        if shuffle:
            random.shuffle(pool)
        if count is not None:
            pool = pool[:count]
        return pool
    def __len__(self):
        '''Return the total number of questions in the bank.'''
        return len(self.questions)