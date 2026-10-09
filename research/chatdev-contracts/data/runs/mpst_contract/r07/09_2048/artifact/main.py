from game import Game2048
from ui import get_key, render

DIRECTIONS = {"left": 0, "up": 1, "right": 2, "down": 3}


def main():
    game = Game2048()
    render(game)
    try:
        while True:
            key = get_key()
            if key == "quit":
                print("Thanks for playing! Score: {} | Highest tile: {}".format(game.score, game.highest))
                break
            if key in DIRECTIONS and game.move(DIRECTIONS[key]):
                render(game)
                if game.game_over():
                    print("Game over! Final score: {} | Highest tile: {}".format(game.score, game.highest))
                    break
    except KeyboardInterrupt:
        print("\nInterrupted! Score: {} | Highest tile: {}".format(game.score, game.highest))


if __name__ == "__main__":
    main()