'''
quiz.py
Core quiz engine: presents questions, collects answers, tracks score,
and reports results (with an optional answer review).
Revision notes:
    - Removed the unused "import random".
    - show_answers_after is now three-state:
        True  -> always show the answer review,
        False -> never show it,
        None  -> ask the user after the quiz (default).
    - _prompt_show_answers() implemented so the review prompt works.
    - Feedback strings are ASCII-only so they print safely on consoles
      that do not use a UTF-8 codec (e.g. Windows cp1252).
'''
class QuizResult:
    """Records the outcome of a single answered question."""
    def __init__(self, number, question, user_answer, is_correct):
        self.number = number
        self.question = question
        self.user_answer = user_answer
        self.is_correct = is_correct
class QuizGame:
    """Runs an interactive quiz session over a list of questions."""
    def __init__(self, questions, show_answers_after=None, input_func=input, output_func=print):
        if not questions:
            raise ValueError("QuizGame requires at least one question.")
        self.questions = list(questions)
        self.show_answers_after = show_answers_after
        self._input = input_func
        self._output = output_func
        self.results = []
    def run(self):
        """Execute the full quiz loop and return the number of correct answers."""
        total = len(self.questions)
        self._output("=" * 60)
        self._output("TRIVIA QUIZ".center(60))
        self._output(f"Answer {total} question{'s' if total != 1 else ''}. Good luck!".center(60))
        self._output("=" * 60)
        for number, question in enumerate(self.questions, start=1):
            self._ask_question(number, question)
        return self.score()
    def _ask_question(self, number, question):
        """Present one question, read the user's answer, and record the result."""
        self._output("")
        self._output(f"Question {number} of {len(self.questions)}  [{question.topic}]")
        self._output(question.display())
        hint = self._answer_hint(question)
        user_answer = self._input(f"Your answer{hint}: ").strip()
        is_correct = question.check_answer(user_answer)
        self.results.append(QuizResult(number, question, user_answer, is_correct))
        if is_correct:
            self._output(">> Correct!")
        else:
            self._output(">> Incorrect.")
    @staticmethod
    def _answer_hint(question):
        if question.type_name == "multiple_choice":
            return " (enter a letter, e.g. A, or the full answer)"
        return ""
    def score(self):
        """Return the number of correctly answered questions."""
        return sum(1 for r in self.results if r.is_correct)
    def display_results(self):
        """Print the final score and, optionally, the answer review."""
        total = len(self.questions)
        correct = self.score()
        percent = (correct / total * 100) if total else 0.0
        self._output("")
        self._output("=" * 60)
        self._output("QUIZ COMPLETE".center(60))
        self._output("=" * 60)
        self._output(f"Total questions : {total}")
        self._output(f"Correct answers : {correct}")
        self._output(f"Score           : {percent:.1f}%")
        if percent == 100:
            self._output("Perfect score! Outstanding!")
        elif percent >= 80:
            self._output("Great job!")
        elif percent >= 50:
            self._output("Not bad - keep practicing!")
        else:
            self._output("Better luck next time!")
        show = self.show_answers_after
        if show is None:
            show = self._prompt_show_answers()
        if show:
            self._display_answer_review()
    def _prompt_show_answers(self):
        """Ask the user whether to review the correct answers."""
        try:
            response = self._input("Review the correct answers? (y/n): ").strip().lower()
        except (EOFError, KeyboardInterrupt, OSError):
            # If input is unavailable, skip the review rather than crash.
            return False
        return response in ("y", "yes")
    def _display_answer_review(self):
        """Show each question with the user's answer and the correct answer."""
        self._output("")
        self._output("-" * 60)
        self._output("ANSWER REVIEW".center(60))
        self._output("-" * 60)
        for result in self.results:
            status = "Correct" if result.is_correct else "Incorrect"
            self._output(f"\nQ{result.number} ({status}) [{result.question.topic}]")
            self._output(f"  Question       : {result.question.text}")
            shown_user = result.user_answer if result.user_answer else "(no answer)"
            self._output(f"  Your answer    : {shown_user}")
            self._output(f"  Correct answer : {result.question.correct_answer_display()}")
            if result.question.explanation:
                self._output(f"  Explanation    : {result.question.explanation}")