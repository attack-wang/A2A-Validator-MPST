class Game:
    def __init__(self):
        self.engine = StoryEngine(get_story())
        self.state = GameState()
    def start(self):
        # show title, intro
        # loop: show node text, show choices, get input, apply effects, transition
    def display_node(self, node): ...
    def display_choices(self, choices, locked): ...
    def get_choice_input(self, num_choices): ...
    def handle_special_commands(self, cmd): ...  # "status", "save", "load", "help", "quit"