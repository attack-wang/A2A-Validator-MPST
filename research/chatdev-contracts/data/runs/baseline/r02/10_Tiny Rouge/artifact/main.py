    def run(self):
        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)
            self.draw()
            self.clock.tick(settings.FPS)
        pygame.quit()
        sys.exit()
if __name__ == "__main__":
    Game().run()