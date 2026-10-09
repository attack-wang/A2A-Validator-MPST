import json
import os

DEFAULT_BANK = [
    {"topic": "Geography", "type": "mc",
     "question": "What is the capital of France?",
     "choices": ["A. London", "B. Paris", "C. Berlin", "D. Madrid"], "answer": "B"},
    {"topic": "Science", "type": "mc",
     "question": "What is H2O commonly known as?",
     "choices": ["A. Salt", "B. Oxygen", "C. Water", "D. Gold"], "answer": "C"},
    {"topic": "Math", "type": "short",
     "question": "What is 7 x 8?", "answer": "56"},
    {"topic": "History", "type": "short",
     "question": "In what year did World War II end?", "answer": "1945"},
    {"topic": "Literature", "type": "mc",
     "question": "Who wrote 'Romeo and Juliet'?",
     "choices": ["A. Dickens", "B. Shakespeare", "C. Tolstoy", "D. Austen"],
     "answer": "B"},
]


def load_questions(path):
    """Load a question bank from a JSON file; fall back to the default bank."""
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict):
                data = data.get("questions", [])
            if isinstance(data, list):
                valid = [q for q in data
                         if isinstance(q, dict)
                         and q.get("question") and q.get("answer")]
                if valid:
                    return valid
            print(f"Warning: '{path}' has no valid questions. Using default bank.")
        except (json.JSONDecodeError, OSError, AttributeError, TypeError,
                ValueError):
            print(f"Warning: could not load '{path}'. Using default bank.")
    return DEFAULT_BANK


class Question:
    def __init__(self, data):
        self.topic = data.get("topic", "General")
        self.type = data.get("type", "mc" if "choices" in data else "short")
        self.text = data["question"]
        self.choices = data.get("choices", [])
        self.answer = str(data["answer"]).strip()

    def is_correct(self, response):
        resp = response.strip().lower()
        if self.type == "mc":
            for choice in self.choices:
                letter = choice.split(".")[0].strip().lower()
                if resp == letter or resp == choice.lower():
                    return True
            return False
        return resp == self.answer.lower()

    def display_answer(self):
        if self.type == "mc" and self.choices:
            for choice in self.choices:
                if choice.split(".")[0].strip().lower() == self.answer.lower():
                    return choice
        return self.answer


class Quiz:
    def __init__(self, questions):
        self.questions = [Question(q) for q in questions]
        self.score = 0
        self.results = []

    def run(self):
        print(f"Trivia Quiz! {len(self.questions)} questions.")
        print("Type your answer and press Enter.\n")
        for i, q in enumerate(self.questions, 1):
            kind = "multiple choice" if q.type == "mc" else "short answer"
            print(f"Question {i} [{q.topic}] ({kind})")
            print(q.text)
            for choice in q.choices:
                print("  " + choice)
            try:
                resp = input("Your answer: ")
            except (EOFError, KeyboardInterrupt):
                print("\nInput ended; finishing quiz with answers so far.")
                break
            correct = q.is_correct(resp)
            self.results.append((q, resp, correct))
            if correct:
                self.score += 1
                print("Correct!\n")
            else:
                print("Incorrect.\n")

    def report(self, show_answers=False):
        print("=" * 40)
        answered = len(self.results)
        line = (f"Quiz complete! Total correct answers: "
                f"{self.score}/{len(self.questions)}")
        if answered < len(self.questions):
            line += f" ({answered} answered)"
        print(line)
        if show_answers:
            print("\nAnswer key:")
            for i, (q, resp, correct) in enumerate(self.results, 1):
                status = "Correct" if correct else f"Your answer: {resp or '(blank)'}"
                print(f"{i}. {q.text}")
                print(f"   Correct answer: {q.display_answer()} ({status})")