class Game:
    """Flappy Bird game: menu, play, death, and game-over states."""
    def __init__(self):
        """Initialize pygame, the window, entities, and persistent best score."""
        pygame.mixer.pre_init(22050, -16, 1, 512)  # must precede pygame.init()
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.sounds = build_sounds()
        self.background = ScrollingBackground()
        self.bird = Bird(BIRD_X, BIRD_START_Y)
        self.pipe_manager = PipeManager()
        self.state = STATE_MENU
        self.score = 0
        self.best = load_best()
        self.flash_alpha = 0
        self.score_pop = 0
        self.gameover_timer = 0
        self.bob_timer = 0
    def run(self):
        """Run the main loop until the user quits."""
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
    def handle_events(self):
        """Process quit, flap, restart, and exit inputs for the current state."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE):
                    pygame.quit()
                    raise SystemExit
                if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                    if self.state == STATE_MENU:
                        self.start_game()
                        self.flap()
                    elif self.state == STATE_PLAYING:
                        self.flap()
                    elif self.state == STATE_GAMEOVER and self.gameover_timer > 30:
                        self.start_game()
                elif event.key == pygame.K_r:
                    if self.state in (STATE_PLAYING, STATE_GAMEOVER, STATE_DYING):
                        self.start_game()
            if event.type == pygame.MOUSEBUTTONDOWN and self.state in (STATE_MENU, STATE_PLAYING):
                if self.state == STATE_MENU:
                    self.start_game()
                self.flap()
    def flap(self):
        """Flap the bird and play the flap sound if available."""
        self.bird.flap()
        self.play_sound("flap")
    def play_sound(self, name):
        """Play a named sound if audio is available."""
        sound = self.sounds.get(name)
        if sound:
            sound.play()
    def start_game(self):
        """Reset all entities and switch to the playing state."""
        self.bird.reset(BIRD_X, BIRD_START_Y)
        self.pipe_manager.reset()
        self.score = 0
        self.flash_alpha = 0
        self.score_pop = 0
        self.gameover_timer = 0
        self.state = STATE_PLAYING
    def die(self):
        """Enter the dying state, flash the screen, and record the best score."""
        self.state = STATE_DYING
        self.flash_alpha = 180
        self.bird.velocity = -4  # small upward hop, classic death flip
        self.play_sound("hit")
        if self.score > self.best:
            self.best = self.score
            save_best(self.best)
    def update(self):
        """Advance the simulation for the current state."""
        if self.state == STATE_MENU:
            # gentle hover animation and slow ambient scroll
            self.bob_timer += 1
            self.bird.y = BIRD_START_Y + math.sin(self.bob_timer * 0.05) * 8
            self.bird.update(animate=True)
            self.background.update(BASE_PIPE_SPEED * 0.4)
        elif self.state == STATE_PLAYING:
            self.bird.update()
            self.pipe_manager.update(self.score)
            self.background.update(self.pipe_manager.speed)
            # scoring
            passed = self.pipe_manager.check_scoring(self.bird.x)
            if passed:
                self.score += passed * SCORE_PER_PIPE
                self.score_pop = 12
                self.play_sound("score")
            # collisions
            if self.bird.get_rect().colliderect(self.ground_rect()):
                self.bird.y = SCREEN_HEIGHT - GROUND_HEIGHT - 12
                self.die()
            elif self.pipe_manager.collides(self.bird.get_rect()):
                self.die()
            # ceiling clamp
            if self.bird.y < self.bird.get_rect().height / 2:  # hmm
                ...
        elif self.state == STATE_DYING:
            self.bird.update(animate=False)
            if self.flash_alpha > 0:
                self.flash_alpha = max(0, self.flash_alpha - 12)
            if self.bird.y >= SCREEN_HEIGHT - GROUND_HEIGHT - 12:
                self.bird.y = SCREEN_HEIGHT - GROUND_HEIGHT - 12
                self.state = STATE_GAMEOVER
                self.gameover_timer = 0
                self.play_sound("die")
        elif self.state == STATE_GAMEOVER:
            self.gameover_timer += 1
            if self.flash_alpha > 0:
                self.flash_alpha = max(0, self.flash_alpha - 12)