'''Quiz orchestration: presenting questions, scoring, and the final report.'''
import config
from utils import ask
class Quiz:
    '''Runs a quiz session over a selected set of questions and tracks the score.'''
    def __init__(self, bank, shuffle=True, show_answers=True):
        '''Store the bank and the session options.'''
        self.bank = bank
        self.shuffle = shuffle
        self.show_answers = show_answers
    def run(self, topic=None, count=None):
        '''Play the quiz and print the final score summary.'''
        resolved_count = count if count is not None else config.DEFAULT_MAX_QUESTIONS
        questions = self.bank.select(topic=topic, count=resolved_count, shuffle=self.shuffle)
        if not questions:
            print("No questions available for this selection. Nothing to play.")
            return
        print("\n=== Trivia Quiz ===")
        print("Questions: {} | Answer with the letter (A-D), the full choice, or free text.".format(len(questions)))
        print("Type 'q' at any prompt to quit early.\n")
        score = 0
        earned = 0
        possible = 0
        results = []
        for number, question in enumerate(questions, start=1):
            possible += question.points
            print("Question {} of {} [{}]".format(number, len(questions), question.topic))
            print(question.display_question())
            user_answer = self._prompt_answer(question)
            if user_answer is None:
                print("\nQuiz ended early by the user.")
                break
            correct = question.check_answer(user_answer)
            results.append((question, user_answer, correct))
            if config.INSTANT_FEEDBACK:
                if correct:
                    print("Correct!\n")
                else:
                    print("Sorry, that is not correct.\n")
            if correct:
                score += 1
                earned += question.points
        self._print_summary(score, earned, possible, results, completed=(len(results) == len(questions)))
    def _prompt_answer(self, question):
        '''Prompt until a non-empty answer is given; None means the user quit.'''
        prompt = "Your answer: "
        while True:
            raw = input(prompt).strip()
            if raw.lower() == "q":
                return None
            if raw:
                return raw
            print("Please enter an answer (or 'q' to quit).")
    def _print_summary(self, score, earned, possible, results, completed):
        '''Print the total correct answers, percentage, and optional review.'''
        answered = len(results)
        print("\n=== Quiz Summary ===")
        if completed:
            print("You answered all {} questions.".format(answered))
        else:
            print("You answered {} of the selected questions before quitting.".format(answered))
        print("Total correct answers: {} / {}".format(score, answered))
        if answered:
            percent = 100.0 * score / answered
            print("Accuracy: {:.1f}%".format(percent))
        if possible:
            print("Points: {} / {}".format(earned, possible))
        if self.show_answers and results:
            print("\n--- Answer Review ---")
            for number, (question, user_answer, correct) in enumerate(results, start=1):
                status = "Correct" if correct else "Incorrect"
                print("{}. [{}] {}".format(number, status, question.display_question().splitlines()[0]))
                print("   Your answer: {}".format(user_answer))
                print("   Correct answer: {}".format(question.display_answer()))