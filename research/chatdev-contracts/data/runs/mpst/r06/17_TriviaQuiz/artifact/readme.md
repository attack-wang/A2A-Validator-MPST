# Trivia Quiz Program
An interactive command-line trivia quiz written in Python. It presents
multiple-choice and short-answer questions, tracks the score, and shows
the total number of correct answers when the quiz ends. Question banks
are configurable JSON files, and you can optionally review the correct
answers after finishing.
## Requirements
- Python 3.6+ (standard library only, no third-party packages)
## Files
| File | Purpose |
|------|---------|
| main.py | Entry point / command-line interface |
| quiz.py | Interactive quiz engine (score tracking, review) |
| question_bank.py | Loads and manages JSON question banks |
| question.py | Question model (validation, answer checking) |
| questions.json | Default sample question bank |
## Usage
Run with the default bank (questions.json):
    python main.py
Use a custom question bank:
    python main.py --bank my_questions.json
Filter by topic, shuffle order, and show the answer review at the end:
    python main.py --bank geography.json --topic Geography --shuffle --show-answers
Get immediate right/wrong feedback after each answer:
    python main.py --bank science.json --feedback
### Command-line options
| Flag | Short | Effect |
|------|-------|--------|
| --bank FILE | -b | Path to a JSON question bank (default: questions.json) |
| --topic TOPIC | -t | Only ask questions from this topic |
| --shuffle | -s | Randomize question order |
| --show-answers | -a | Always show the answer review after the quiz |
| --feedback | -f | Show immediate right/wrong feedback per question |
### Playing
Type your answer and press Enter. For multiple-choice questions you may
answer with the choice letter (e.g. B) or the full choice text. Type 'q'
at any prompt to quit early. When the quiz ends, the total number of
correct answers is displayed, and you are offered an answer review
(unless --show-answers was given, in which case the review is shown
automatically).
## Custom Question Banks
A question bank is a JSON file of the form:
    {
      "title": "My Quiz",
      "questions": [
        {
          "type": "multiple_choice",
          "question": "What is the capital of France?",
          "choices": ["London", "Paris", "Berlin", "Madrid"],
          "answer": "Paris",
          "explanation": "Paris has been France's capital for centuries.",
          "topic": "Geography"
        },
        {
          "type": "short_answer",
          "question": "What is 7 x 8?",
          "answer": "56",
          "accept": ["fifty-six"],
          "topic": "Math"
        }
      ]
    }
Field notes:
- type: multiple_choice (aliases: mc, choice) or short_answer
  (aliases: short, sa, text).
- choices: required for multiple-choice (at least 2 options).
- answer: the correct answer (required).
- accept: optional list (or a single string) of alternate accepted
  answers, e.g. "accept": ["William Shakespeare"].
- explanation, topic: optional.
Answer matching is case-insensitive and ignores punctuation and spacing.