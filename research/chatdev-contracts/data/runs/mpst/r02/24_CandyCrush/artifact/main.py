    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self._on_click(event.pos)
            self._update(dt)
            self.screen.fill(COLOR_BACKGROUND)
            self._draw_hud()
            self._draw_board()
            self._draw_candies()
            self._draw_selection()
            self._draw_game_over()
            pygame.display.flip()
        pygame.quit()
def main():
    GameGUI().run()
if __name__ == "__main__":
    main()