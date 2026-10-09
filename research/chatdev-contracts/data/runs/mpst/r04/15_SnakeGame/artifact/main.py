def main():
    pygame.init()
    high_score = 0
    try:
        while True:
            choice = Menu().show()
            if choice == "quit":
                break
            game = Game(choice, high_score)
            result = game.run()
            high_score = max(high_score, game.score)
            if result == "quit":
                break
    finally:
        pygame.quit()
    sys.exit(0)