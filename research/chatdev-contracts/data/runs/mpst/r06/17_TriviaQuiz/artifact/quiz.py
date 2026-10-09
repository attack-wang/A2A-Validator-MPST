'''
quiz.py
Runs an interactive trivia quiz session in the terminal: presents each
question, reads the user's answer, tracks the score, prints the final
result and optionally reviews every question with the correct answer.
'''
from question import Question  # noqa: F401  (kept for type documentation)
class Quiz:
    """Interactive trivia quiz engine."""
    def __init__(self, question_bank, show_answers_after=False, immediate_feedback=False, input_fn=input, output_fn=print):
        self.bank = question_bank
        self.show_answers_after = show_answers_after
        self.immediate_feedback = immediate_feedback
        self._input = input_fn
        self._print = output_fn
        self.score = 0
        self.results = []  # list of dicts: number, question, user_answer, correct
    def run(self):
        """Run the full quiz session and return the final score."""
        questions = self.bank.questions
        total = len(questions)
        self._print()
        self._print("=" * 60)
        self._print(f"  {self.bank.title}")
        self._print(f"  {total} question(s) | Topics: {', '.join(self.bank.topics())}")
        self._print("=" * 60)
        self._print("Instructions: type your answer and press Enter.")
        self._print("For multiple-choice questions, you may answer with the")
        self._print("choice letter (e.g. 'B') or the full choice text.")
        self._print("Type 'q' at any prompt to quit early.")
        self._print("-" * 60)
        for number, question in enumerate(questions, start=1):
            user_answer = self._ask_question(number, total, question)
            if user_answer is None:  # user quit
                break
            correct = question.is_correct(user_answer)
            self.results.append({
                "number": number,
                "question": question,
                "user_answer": user_answer,
                "correct": correct,
            })
            if correct:
                self.score += 1
            if self.immediate_feedback:
                if correct:
                    self._print("✔ Correct!")
                else:
                    self._print(f"✘ Incorrect. The correct answer is: {question.correct_answer_display()}")
                self._print()
        self.display_results()
        if self.show_answers_after:
            self.review_answers()
        else:
            self._offer_review()
        return self.score
    def _ask_question(self, number, total, question):
        """Display one question and read the user's answer. None means quit."""
        self._print()
        self._print(f"Question {number} of {total}  [{question.topic}]")
        self._print(question.display())
        prompt = "Your answer: " if question.q_type == "short_answer" else "Your answer (letter or text): "
        while True:
            try:
                answer = self._input(prompt).strip()
            except (EOFError, KeyboardInterrupt):
                self._print()
                return None
            if answer.lower() == "q":
                return None
            if answer == "":
                self._print("Please enter an answer (or 'q' to quit).")
                continue
            return answer
    def display_results(self):
        """Print the final score summary."""
        total = len(self.results)
        self._print()
        self._print("=" * 60)
        self._print("  QUIZ COMPLETE" if total == len(self.bank.questions) else "  QUIZ ENDED EARLY")
        self._print("=" * 60)
        percent = (self.score / total * 100) if total else 0.0
        self._print(f"Total correct answers: {self.score} out of {total} ({percent:.1f}%)")
        self._print(self._verdict(percent))
    @staticmethod
    def _verdict(percent):
        """Map a percentage score onto a friendly closing remark."""
        if percent == 100:
            return "Perfect score! Outstanding!"
        if percent >= 80:
            return "Great job!"
        if percent >= 60:
            return "Not bad — keep practicing!"
        if percent >= 40:
            return "Room for improvement."
        return "Better luck next time!"
    def review_answers(self):
        """Print a full review of every question with the correct answer."""
        self._print()
        self._print("-" * 60)
        self._print("ANSWER REVIEW")
        self._print("-" * 60)
        for result in self.results:
            question = result["question"]
            marker = "✔" if result["correct"] else "✘"
            self._print()
            self._print(f"{marker} Q{result['number']}: {question.text}")
            if question.q_type == "multiple_choice":
                for index, choice in enumerate(question.choices):
                    self._print(f"     {chr(ord('A') + index)}) {choice}")
            self._print(f"   Your answer: {result['user_answer']}")
            self._print(f"   Correct answer: {question.correct_answer_display()}")
            if question.explanation:
                self._print(f"   Note: {question.explanation}")
    def _offer_review(self):
        """Ask the user whether they want to see the correct answers."""
        try:
            choice = self._input("Would you like to see the correct answers? (y/n): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            choice = "n"
        if choice in ("y", "yes"):
            self.review_answers()