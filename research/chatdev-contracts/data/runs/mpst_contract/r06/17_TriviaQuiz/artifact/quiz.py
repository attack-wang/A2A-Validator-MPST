"""Question and Quiz engine for the trivia program."""
import random


class Question:
    def __init__(self, text, qtype, answer, options=None, topic="General", accepts=None):
        self.text = text
        self.qtype = qtype  # "mc" (multiple choice) or "short" (short answer)
        self.options = list(options or [])
        self.answer = answer
        self.topic = topic
        self.accepts = list(accepts or [])

    def check(self, user_input):
        s = str(user_input).strip()
        if self.qtype == "mc":
            u = s.upper()
            if len(u) == 1 and u.isalpha():
                idx = ord(u) - 65
                if 0 <= idx < len(self.options):
                    return idx == self.answer
            if s.isdigit():
                idx = int(s) - 1
                if 0 <= idx < len(self.options):
                    return idx == self.answer
            return s.lower() == self.options[self.answer].strip().lower()
        u = s.lower()
        return u == str(self.answer).strip().lower() or u in (
            a.strip().lower() for a in self.accepts
        )

    def correct_display(self):
        if self.qtype == "mc":
            return f"{chr(65 + self.answer)}) {self.options[self.answer]}"
        return str(self.answer)

    def render(self, number):
        lines = [f"Q{number}. [{self.topic}] {self.text}"]
        if self.qtype == "mc":
            for i, opt in enumerate(self.options):
                lines.append(f"   {chr(65 + i)}) {opt}")
            lines.append("Your answer (letter or number):")
        else:
            lines.append("Your answer:")
        return "\n".join(lines)


class Quiz:
    def __init__(self, questions, shuffle=False):
        self.questions = list(questions)
        self.score = 0
        self.results = []  # (question, user_answer, was_correct)
        if shuffle:
            random.shuffle(self.questions)

    def run(self, prompt=input, echo=print):
        echo(f"Starting quiz: {len(self.questions)} questions. Type an answer and press Enter.\n")
        for i, q in enumerate(self.questions, 1):
            echo(q.render(i))
            try:
                ans = prompt("> ")
            except (EOFError, KeyboardInterrupt):
                echo("\nQuiz interrupted.")
                break
            ok = q.check(ans)
            self.results.append((q, ans, ok))
            echo("Correct!\n" if ok else "Wrong.\n")
            if ok:
                self.score += 1

    def summary(self):
        answered = len(self.results)
        total = len(self.questions)
        pct = (self.score / answered * 100) if answered else 0.0
        text = f"Quiz complete! Total correct answers: {self.score}/{answered} ({pct:.1f}%)"
        if answered < total:
            text += f" - {total - answered} question(s) unanswered."
        return text

    def review(self):
        lines = ["--- Answer Review ---"]
        for i, (q, ans, ok) in enumerate(self.results, 1):
            status = "Correct" if ok else "Incorrect"
            lines.append(
                f"Q{i}. {status} | Your answer: {ans!r} | Correct answer: {q.correct_display()}"
            )
        return "\n".join(lines)