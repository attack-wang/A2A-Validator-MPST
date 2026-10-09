'''
Entry point for the Mastermind code-breaking game.
Wires together the configuration, game engine, and console UI, and
runs the main game loop (including replay support and graceful quit
via the QuitGame exception).
'''
from config import GameConfig
from game_engine import GameEngine
from ui import ConsoleUI, QuitGame
from validator import GuessValidator
def play_one_game(engine, ui, validator):
    '''
    Run a single full game session from start to finish.
    :raises QuitGame: if the player chooses to quit mid-game
    '''
    engine.start_new_game()
    ui.show_welcome()
    ui.show_rules()
    while not engine.is_over():
        ui.show_board(engine.board)
        guess = ui.prompt_guess(validator, engine.attempts_used + 1)
        feedback = engine.make_guess(guess)
        ui.show_feedback(feedback)
    ui.show_board(engine.board)
    if engine.won:
        ui.show_win(engine.secret, engine.attempts_used)
    else:
        ui.show_lose(engine.secret)
def main():
    '''Set up all components and run the replay loop.'''
    config = GameConfig.classic()
    engine = GameEngine(config)
    ui = ConsoleUI(config)
    validator = GuessValidator(config.colors.keys(), config.code_length)
    while True:
        try:
            play_one_game(engine, ui, validator)
        except QuitGame:
            print("\nGame aborted by player. The secret code was: "
                  f"{' '.join(engine.secret)}")
            break
        if not ui.ask_replay():
            ui.show_goodbye()
            break
if __name__ == "__main__":
    main()