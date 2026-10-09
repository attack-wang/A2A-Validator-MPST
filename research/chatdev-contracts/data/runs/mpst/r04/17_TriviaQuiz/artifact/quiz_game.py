'''
quiz_game.py
Core game engine for the trivia quiz program.
Presents questions, reads and validates user answers, tracks the score,
and produces the end-of-quiz summary including the optional answer review.
Input/output functions are injectable, which makes the game easy to test.
'''
import random
from question import Question
class QuizGame:
    """Runs a quiz session over a question bank and tracks the score."""
    def __init__(self, bank, shuffle_questions=False, shuffle_options=False,
                 show_answers=True, input_func=input, output_func=print):
        self.bank = bank
        self.shuffle_questions = shuffle_questions
        self.shuffle_options = shuffle_options
        self.show_answers = show_answers
        self._input = input_func
        self._print = output_func
        self.results = []  # list of dicts: {"question", "user_answer", "is_correct"}
        self.correct_count = 0
    def run(self):
        """Run the full quiz loop, then show the summary and optional review."""
        questions = list(self.bank.questions)
        if self.shuffle_questions:
            random.shuffle(questions)
        total = len(questions)
        self._print("=" * 60)
        self._print(f"QUIZ: {self.bank.name}  ({total} question{'s' if total != 1 else ''})")
        self._print("=" * 60)
        for idx, question in enumerate(questions, start=1):
            if self.shuffle_options and question.question_type == Question.MULTIPLE_CHOICE:
                question = question.copy_with_shuffled_options()
            user_answer = self._ask_question(idx, question, total)
            is_correct = question.check_answer(user_answer)
            self.results.append(
                {"question": question, "user_answer": user_answer, "is_correct": is_correct}
            )
            self._print("Correct!" if is_correct else "Incorrect.")
            if is_correct:
                self.correct_count += 1
        self.display_summary()
        if self.show_answers:
            self.review_answers()
    def _ask_question(self, index, question, total):
        """Display one question and loop until a non-empty answer is given."""
        self._print(f"\nQuestion {index} of {total} [{question.topic}]")
        self._print(question.text)
        if question.question_type == Question.MULTIPLE_CHOICE:
            for letter, option in zip(Question.LETTERS, question.options):
                self._print(f"  {letter}) {option}")
            prompt = "Your answer (letter or text): "
        else:
            prompt = "Your answer: "
        while True:
            answer = self._input(prompt).strip()
            if answer:
                return answer
            self._print("Please enter a non-empty answer.")
    def display_summary(self):
        """Print the final score summary required by the task."""
        total = len(self.results)
        percent = (self.correct_count / total * 100) if total else 0.0
        self._print("\n" + "=" * 60)
        self._print("QUIZ COMPLETE")
        self._print(f"Question bank     : {self.bank.name}")
        self._print(f"Questions asked   : {total}")
        self._print(f"Correct answers   : {self.correct_count}")
        self._print(f"Incorrect answers : {total - self.correct_count}")
        self._print(f"Final score       : {percent:.0f}%")
        self._print("=" * 60)
    def review_answers(self):
        """Optionally show the correct answer for every question (task option)."""
        self._print("\nANSWER REVIEW")
        self._print("-" * 60)
        for idx, result in enumerate(self.results, start=1):
            question = result["question"]
            self._print(f"\n{idx}. [{'Correct' if result['is_correct'] else 'Incorrect'}] {question.text}")
            self._print(f"   Your answer : {result['user_answer']}")
            self._print(f"   Correct     : {question.correct_answer_display}")
            if question.explanation:
                self._print(f"   Info        : {question.explanation}")