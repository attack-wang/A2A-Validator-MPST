'''
input_handler.py
'''
from display import ...
class InputHandler:
    def __init__(self, word_manager, input_func=input, output=print):
        ...
    def get_guess(self):
        while True:
            raw = input prompt
            normalized
            checks:
              empty -> message
              not 5 -> message
              not alpha -> message
              not in dictionary -> message
            return word