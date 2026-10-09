'''
quiz.py
Contains the QuizEngine class, which runs an interactive quiz session:
it presents questions, reads and validates user answers, tracks the score,
prints the final result and can review the correct answers afterwards.
'''
from questions import MultipleChoiceQuestion
class QuizEngine:
    """Runs one full quiz session over a list of questions."""
    def __init__(self, questions, show_answers_after=False, input_func=input, output_func=print):
        """Prepare the quiz session.
        questions: non-empty list of Question objects (order as given).
        show_answers_after: if True, always show the answer review; if False,
            ask the user interactively after the results summary.
        input_func/output_func: injectable I/O for testing.
        """
        if not questions:
            raise ValueError("QuizEngine needs at least one question.")
        self.questions = list(questions)
        self.show_answers_after = show_answers_after
        self._input = input_func
        self._output = output_func
        self.score = 0
        self.points_possible = sum(q.points for q in self.questions)
        self.points_earned = 0
        self.record = []