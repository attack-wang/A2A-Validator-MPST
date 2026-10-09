'''
quiz.py
Implements the interactive quiz session: presenting questions, reading
user answers, tracking the score, and displaying results. The session can
be interrupted with Ctrl+C (KeyboardInterrupt) or Ctrl+D/EOF, in which case
partial results are still shown.
'''
from question import Question
from score_tracker import ScoreTracker
class Quiz:
    """Runs an interactive trivia quiz session."""
    def __init__(self, question_bank, questions=None, show_answers_after=False, input_func=None, output_func=None):
        """Prepare the quiz with a bank, an optional question list, and I/O hooks."""
        self.bank = question_bank
        self.questions = questions if questions is not None else question_bank.select()
        self.show_answers_after = show_answers_after
        self.tracker = ScoreTracker()
        self._input = input_func or input
        self._output = output_func or print
        self._interrupted = False
    def run(self):
        """Present every question, record results, then display the results."""
        self._show_header()
        total = len(self.questions)
        for index, question in enumerate(self.questions, start=1):
            try:
                user_answer = self._ask_question(index, total, question)
            except (KeyboardInterrupt, EOFError):
                self._interrupted = True
                self._output("\n\nQuiz interrupted by user. Ending early...")
                break
            is_correct = question.check_answer(user_answer)
            self.tracker.record(question, user_answer, is_correct)
            if is_correct:
                self._output("Correct!")
            else:
                self._output("Incorrect.")
            self._output("")
        self._display_results()
    def _show_header(self):
        """Print the quiz header with the bank title and question count."""
        self._output("=" * 50)
        self._output(f"Welcome to: {self.bank.title}")
        self._output(f"Questions: {len(self.questions)}")
        self._output("Type your answer and press Enter. (Ctrl+C to quit)")
        self._output("=" * 50)
    def _ask_question(self, index, total, question):
        """Print one question and read a non-empty answer from the user."""
        self._output(f"\nQuestion {index} of {total}  [{question.topic}]")
        self._output(question.text)
        if question.question_type == Question.MULTIPLE_CHOICE:
            self._output(question.format_choices())
            prompt = "Your answer (letter or full choice): "
        else:
            prompt = "Your answer: "
        while True:
            answer = self._input(prompt).strip()
            if answer:
                return answer
            self._output("Please enter a non-empty answer (or press Ctrl+C to quit).")
    def _display_results(self):
        """Print the final score and, optionally, the full answer review."""
        self._output("=" * 50)
        self._output("QUIZ COMPLETE" if not self._interrupted else "QUIZ ENDED EARLY")
        self._output(self.tracker.summary())
        if self.show_answers_after:
            self._output("\n--- Answer Review ---")
            for line in self.tracker.review_lines():
                self._output(line)
        self._output("=" * 50)
        self._output("Thanks for playing!")