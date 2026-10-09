'''
Quiz engine: runs through questions, tracks score and results.
The Quiz class is agnostic of the user interface: it receives questions,
accepts submitted answers, and exposes score/result data for display.
'''
class Quiz:
    def __init__(self, questions, immediate_feedback=False):
        self.questions = list(questions)
        self.immediate_feedback = immediate_feedback
        self.current_index = 0
        self.results = []  # list of dicts: question, user_answer, correct(bool)
    @property
    def score(self):
        return sum(1 for r in self.results if r["correct"])
    @property
    def total_answered(self):
        return len(self.results)
    def has_next(self):
        return self.current_index < len(self.questions)
    def current_question(self):
        if self.has_next():
            return self.questions[self.current_index]
        return None
    def submit_answer(self, user_answer):
        question = self.current_question()
        if question is None:
            raise RuntimeError("No question to answer")
        correct = question.check_answer(user_answer)
        self.results.append({
            "question": question,
            "user_answer": user_answer,
            "correct": correct,
        })
        self.current_index += 1
        return correct
    def is_finished(self):
        return self.current_index >= len(self.questions)
    def final_score(self):
        return self.score, len(self.questions)
    def percentage(self):
        if not self.questions:
            return 0.0
        return 100.0 * self.score / len(self.questions)
    def topic_breakdown(self):
        breakdown = {}
        for r in self.results:
            topic = r["question"].topic
            stats = breakdown.setdefault(topic, {"correct": 0, "total": 0})
            stats["total"] += 1
            if r["correct"]:
                stats["correct"] += 1
        return breakdown