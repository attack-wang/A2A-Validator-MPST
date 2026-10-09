class Quiz:
    def __init__(self, questions, ui, show_answers_after=False):
        self.questions = list(questions)
        self.ui = ui
        self.show_answers_after = show_answers_after
        self.result = QuizResult()
    def run(self):
        self.ui.show_intro(len(self.questions))
        quit_requested = False
        for number, question in enumerate(self.questions, start=1):
            outcome = self._ask_question(number, question)
            if outcome is None:
                quit_requested = True
                break
        self._finish(quit_requested)
    def _ask_question(self, number, question):
        self.ui.show_message()
        header = f"Question {number} of {len(self.questions)} [{question.topic}]"
        self.ui.show_message(header)
        self.ui.show_message("-" * len(header))
        self.ui.show_message(question.text)
        if isinstance(question, MultipleChoiceQuestion):
            for index, choice in enumerate(question.choices):
                letter = MultipleChoiceQuestion.LETTERS[index]
                self.ui.show_message(f"  {letter}) {choice}")
        user_answer = self.ui.prompt_answer(question)
        if user_answer is None:
            return None
        correct = question.check_answer(user_answer)
        self.result.record(question, user_answer, correct)
        if correct:
            self.ui.show_message("Correct!")
        else:
            self.ui.show_message(f"Sorry, the correct answer was: {question.answer}")
        return correct
    def _finish(self, quit_requested=False):
        self.ui.show_message()
        self.ui.show_message("=" * 60)
        if quit_requested:
            self.ui.show_message("Quiz ended early at your request.")
        self.ui.show_message(self.result.summary())
        self.ui.show_message("=" * 60)
        show_review = self.show_answers_after
        if not show_review and self.result.records:
            show_review = self.ui.confirm("Review the correct answers?", default=False)
        if show_review:
            self._show_review()
    def _show_review(self):
        self.ui.show_message()
        self.ui.show_message("ANSWER REVIEW")
        self.ui.show_message("-" * 60)
        for index, record in enumerate(self.result.records, start=1):
            question = record["question"]
            status = "correct" if record["correct"] else "incorrect"
            self.ui.show_message(f"{index}. {question.text}")
            self.ui.show_message(f"   Your answer  : {record['user_answer'] or '(quit)'}")
            self.ui.show_message(f"   Correct answer: {question.answer}")
            self.ui.show_message(f"   Result       : {status}")