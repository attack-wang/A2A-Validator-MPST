'''
main.py
Entry point for the Mastermind game.
Wires the configuration, console UI and game engine together, plays
complete rounds (secret generation, attempt-limited guessing with
exact/partial peg feedback, explicit win/lose outcome) and offers the
player to replay until they choose to quit.
'''
from config import GameConfig
from game_engine import GameEngine
from ui import ConsoleUI
def play_one_round(config, ui):
    '''
    Play one full round: roll a new secret, run the guess loop and
    announce the win/lose outcome.
    Args:
        config: GameConfig instance with palette/length/attempts.
        ui: ConsoleUI instance used for all interaction.
    '''
    engine = GameEngine(config)
    engine.start()
    while not engine.game_over:
        ui.show_attempts_left(engine.attempts_remaining)
        try:
            guess = ui.prompt_guess(engine.attempts_used + 1)
        except EOFError:
            ui.show_error('Input closed -- the hidden code was: %s'
                          % ' '.join(engine.secret))
            return
        feedback = engine.submit_guess(guess)
        ui.show_guess_result(guess, feedback)
    if engine.won:
        ui.show_win(engine.attempts_used)
    else:
        ui.show_lose(engine.secret)
def main():
    '''Configure the game and run the replay loop.'''
    config = GameConfig()
    ui = ConsoleUI(config)
    ui.show_welcome()
    while True:
        play_one_round(config, ui)
        if not ui.ask_play_again():
            break
    ui.show_goodbye()
if __name__ == '__main__':
    main()