"""Built-in configurable question bank.

Each entry:
  {"topic": str, "type": "mc", "question": str, "choices": [str, ...], "answer": str}
  {"topic": str, "type": "sa", "question": str, "answer": str or [str, ...]}

Edit this list or supply a JSON file via: python main.py --bank mybank.json
"""

QUESTION_BANK = [
    {"topic": "Geography", "type": "mc", "question": "What is the capital of Australia?",
     "choices": ["Sydney", "Melbourne", "Canberra", "Perth"], "answer": "Canberra"},
    {"topic": "Geography", "type": "sa", "question": "What is the longest river in the world?",
     "answer": ["nile", "the nile"]},
    {"topic": "Science", "type": "mc", "question": "What is the chemical symbol for gold?",
     "choices": ["Go", "Gd", "Au", "Ag"], "answer": "Au"},
    {"topic": "Science", "type": "sa", "question": "How many planets are in our solar system?",
     "answer": ["8", "eight"]},
    {"topic": "History", "type": "mc", "question": "In which year did World War II end?",
     "choices": ["1943", "1945", "1947", "1950"], "answer": "1945"},
    {"topic": "History", "type": "sa", "question": "Who was the first President of the United States?",
     "answer": ["george washington", "washington"]},
    {"topic": "Literature", "type": "mc", "question": "Who wrote 'Romeo and Juliet'?",
     "choices": ["Charles Dickens", "William Shakespeare", "Jane Austen", "Mark Twain"],
     "answer": "William Shakespeare"},
    {"topic": "Literature", "type": "sa", "question": "What is the first book of the 'Lord of the Rings' trilogy?",
     "answer": ["the fellowship of the ring", "fellowship of the ring"]},
    {"topic": "Math", "type": "sa", "question": "What is 12 x 8?",
     "answer": ["96"]},
    {"topic": "Math", "type": "mc", "question": "What is the value of pi to two decimal places?",
     "choices": ["3.12", "3.14", "3.16", "3.18"], "answer": "3.14"},
    {"topic": "Technology", "type": "mc", "question": "What does 'CPU' stand for?",
     "choices": ["Central Process Unit", "Computer Personal Unit",
                 "Central Processing Unit", "Core Program Utility"],
     "answer": "Central Processing Unit"},
    {"topic": "Technology", "type": "sa", "question": "Which programming language is named after a TV comedy group?",
     "answer": ["python"]},
    {"topic": "Sports", "type": "mc", "question": "How many players are on a soccer team on the field?",
     "choices": ["9", "10", "11", "12"], "answer": "11"},
    {"topic": "Music", "type": "sa", "question": "How many strings does a standard guitar have?",
     "answer": ["6", "six"]},
]