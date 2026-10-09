"""Quiz engine: question model, answer checking, scoring, and post-quiz review."""

from dataclasses import dataclass, field


@dataclass
class Question:
    topic: str
    text: str
    qtype: str  # "multiple_choice" or "short_answer"
    answer: str
    choices: list = field(default_factory=list)

    @staticmethod
    def normalize(value):
        return " ".join(str(value).strip().lower().split())

    def _choice_for(self, token):
        """Return the choice text matching a letter (a/b/c...) or number (1/2/3...)."""
        if len(token) == 1:
            if "a" <= token <= "z":
                index = ord(token) - ord("a")
                if 0 <= index < len(self.choices):
                    return self.choices[index]
            if token.isdigit():
                index = int(token) - 1
                if 0 <= index < len(self.choices):
                    return self.choices[index]
        return None

    def is_correct(self, response):
        response = self.normalize(response)
        if not response:
            return False
        correct = self.normalize(self.answer)
        if response == correct:
            return True
        if self.qtype != "multiple_choice":
            return False
        picked = self._choice_for(response)
        if picked is not None:
            if self.normalize(picked) == correct:
                return True
            answer_choice = self._choice_for(correct)
            return answer_choice is not None and self.normalize(answer_choice) == self.normalize(picked)
        answer_choice = self._choice_for(correct)
        return answer_choice is not None and self.normalize(answer_choice) == response

    def correct_answer_text(self):
        if self.qtype == "multiple_choice":
            answer_choice = self._choice_for(self.normalize(self.answer))
            if answer_choice is not None:
                letter = chr(ord("A") + self.choices.index(answer_choice))
                return f"{letter}) {answer_choice}"
        return str(self.answer)

    def prompt_lines(self):
        lines = [f"[{self.topic} - {self.qtype.replace('_', ' ')}]", self.text]
        if self.qtype == "multiple_choice":
            for index, choice in enumerate(self.choices):
                lines.append(f"  {chr(ord('A') + index)}) {choice}")
        return lines


class Quiz:
    def __init__(self, questions, show_answers=False, input_fn=input, output_fn=print):
        self.questions = questions
        self.show_answers = show_answers
        self._input = input_fn
        self._print = output_fn
        self.results = []

    def run(self):
        total = len(self.questions)
        self._print("=" * 55)
        self._print("TRIVIA QUIZ".center(55))
        self._print("=" * 55)
        for number, question in enumerate(self.questions, 1):
            self._print("")
            self._print(f"Question {number} of {total}")
            for line in question.prompt_lines():
                self._print(line)
            hint = " (letter or text)" if question.qtype == "multiple_choice" else ""
            try:
                response = self._input(f"Your answer{hint}: ").strip()
            except EOFError:
                response = ""
            correct = question.is_correct(response)
            self.results.append(
                {"number": number, "question": question,
                 "response": response, "correct": correct}
            )
            self._print("Correct!" if correct else "Incorrect.")
        self._print("")
        self._print("=" * 55)
        self._print(f"Quiz finished! Total correct answers: {self.score()}/{total}")
        self._print("=" * 55)
        if self.show_answers:
            self.review()

    def score(self):
        return sum(1 for result in self.results if result["correct"])

    def review(self):
        self._print("")
        self._print("Correct answers review:")
        for result in self.results:
            question = result["question"]
            status = "CORRECT" if result["correct"] else "WRONG"
            self._print(f"{result['number']}. ({status}) {question.text}")
            self._print(f"   Your answer:    {result['response'] or '(blank)'}")
            self._print(f"   Correct answer: {question.correct_answer_text()}")