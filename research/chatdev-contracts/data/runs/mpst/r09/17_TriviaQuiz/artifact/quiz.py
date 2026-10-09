'''
quiz.py
Quiz engine for the ChatDev Trivia Quiz.
Runs the list of Question objects one by one, collects and grades the
user's answers, tracks the running score, optionally gives immediate
per-question feedback, and finishes with a summary showing the total
number of correct answers plus a configurable answer review.
The user may quit early at any prompt by typing Q, QUIT or EXIT.
This module defines BOTH QuitQuiz and the previously missing Quiz class
so that "from quiz import Quiz" in main.py resolves correctly.
'''
from question import Question
class QuitQuiz(Exception):
    """Raised internally when the user chooses to quit the quiz early."""
class Quiz:
    """Runs a list of Question objects, tracks the score, and reports results."""
    QUIT_TOKENS = {"Q", "QUIT", "EXIT"}
    def __init__(self, questions, immediate_feedback=True,
                 show_answers_at_end=True, input_func=input, output_func=print):
        """Store questions and I/O hooks; validate the quiz is runnable."""
        if not questions:
            raise ValueError("Quiz requires at least one question.")
        self._questions = list(questions)
        self._immediate_feedback = immediate_feedback
        self._show_answers_at_end = show_answers_at_end
        self._input = input_func
        self._output = output_func
        self._results = []  # list of (index, question, user_answer, correct)
    def run(self):
        """Ask every question, grade answers, then print the final summary."""
        total = len(self._questions)
        self._output("=" * 60)
        self._output("ChatDev Trivia Quiz")
        self._output(f"{total} question(s). Type your answer; 'Q' quits early.")
        self._output("=" * 60)
        score = 0
        for index, question in enumerate(self._questions, start=1):
            try:
                user_answer = self._ask_question(index, total, question)
            except QuitQuiz:
                self._output("\nQuiz ended early by user.")
                break
            except (EOFError, KeyboardInterrupt):
                self._output("\nInput interrupted - ending quiz.")
                break
            correct = question.is_correct(user_answer)
            self._results.append((index, question, user_answer, correct))
            if correct:
                score += 1
            if self._immediate_feedback:
                if correct:
                    self._output("Correct!")
                else:
                    self._output(
                        f"Incorrect. Correct answer: {question.correct_answer_display()}"
                    )
        self._show_final_results(score)
        return score
    def _ask_question(self, index, total, question):
        """Display one question, read the answer, and handle quit requests."""
        self._output("")
        self._output(f"Question {index} of {total}  [{question.topic}]")
        self._output(question.display())
        if question.question_type == Question.MULTIPLE_CHOICE:
            prompt = "Your answer (letter or text, Q to quit): "
        else:
            prompt = "Your answer (Q to quit): "
        raw = self._input(prompt)
        if raw is None:
            raise EOFError
        raw = str(raw).strip()
        if raw.upper() in self.QUIT_TOKENS:
            raise QuitQuiz
        return raw if raw else "(no answer)"
    def _show_final_results(self, score):
        """Print total correct answers and the optional answer review."""
        total = len(self._questions)
        self._output("")
        self._output("=" * 60)
        self._output("Quiz complete!")
        self._output(f"Total correct answers: {score} / {total}")
        if total:
            self._output(f"Score: {score / total * 100:.0f}%")
        if self._show_answers_at_end:
            self._output("")
            self._output("Answer review:")
            for index, question, user_answer, correct in self._results:
                mark = "[CORRECT]" if correct else "[WRONG]"
                self._output(f"  {mark} Q{index}: {question.text}")
                self._output(f"      Your answer:    {user_answer}")
                self._output(
                    f"      Correct answer: {question.correct_answer_display()}"
                )
        self._output("=" * 60)