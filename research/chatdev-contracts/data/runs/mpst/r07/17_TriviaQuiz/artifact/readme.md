# ChatDev Trivia Quiz
A command-line trivia quiz program written in Python. It presents
multiple-choice and short-answer questions from a configurable JSON
question bank, tracks the score while you play, and displays the total
correct answers when the quiz is finished.
## Features
- Multiple-choice questions: answer with a choice letter (e.g. `B`) or the full choice text.
- Short-answer questions: case-insensitive text comparison, multiple accepted answers supported.
- Configurable question banks: load any JSON question bank file at startup.
- Topic selection and configurable number of questions per session.
- Score tracking with a final summary: total questions, correct answers, percentage, and letter grade.
- Optional answer review that reveals the correct answers after the quiz.
## Project Files
| File | Purpose |
| --- | --- |
| main.py | Entry point: welcome banner and play-again loop |
| session.py | One quiz session: bank loading, topic/count/answer options |
| question_bank.py | Loads questions from JSON; topic filter, shuffle, count |
| question.py | Question class: validation, formatting, answer checking |
| quiz.py | Quiz engine: asks questions, tracks score, results, review |
| questions.json | Default sample question bank |
## How to Run
Requires Python 3.6 or later. No third-party dependencies.
    python main.py
Then follow the prompts:
1. Enter the path to a question bank JSON file (press Enter for the default `questions.json`).
2. Pick a topic (or all topics).
3. Choose how many questions to answer.
4. Decide whether correct answers should be displayed after the quiz.
5. Answer each question and see your final score.
## Question Bank Format
Question banks are JSON files with a top-level `questions` list. Example:
    {
      "questions": [
        {
          "question": "Which planet is known as the Red Planet?",
          "type": "multiple_choice",
          "choices": ["Venus", "Mars", "Jupiter", "Saturn"],
          "answer": "Mars",
          "topic": "Science"
        },
        {
          "question": "What is the capital of France?",
          "type": "short_answer",
          "answer": ["paris"],
          "topic": "Geography"
        }
      ]
    }
Field reference:
- `question` (string, required): the question text.
- `type` (string, required): `multiple_choice` or `short_answer`.
- `choices` (list of strings): required for multiple-choice questions (at least two choices).
- `answer` (string or list of strings): the correct answer. A list means several acceptable answers, which is useful for short-answer questions.
- `topic` (string, optional): category label; defaults to `General`.
To use your own bank, save it as a `.json` file and enter its path when the
program prompts for a question bank file.