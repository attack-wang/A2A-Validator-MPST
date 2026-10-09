import argparse
from quiz import Quiz, load_questions


def main():
    parser = argparse.ArgumentParser(description="Trivia Quiz Program")
    parser.add_argument("--bank", default="questions.json",
                        help="Path to a JSON question bank file")
    parser.add_argument("--show-answers", action="store_true",
                        help="Display correct answers after the quiz")
    args = parser.parse_args()

    questions = load_questions(args.bank)
    if not questions:
        print("No valid questions found in the question bank.")
        return

    quiz = Quiz(questions)
    quiz.run()
    quiz.report(show_answers=args.show_answers)


if __name__ == "__main__":
    main()