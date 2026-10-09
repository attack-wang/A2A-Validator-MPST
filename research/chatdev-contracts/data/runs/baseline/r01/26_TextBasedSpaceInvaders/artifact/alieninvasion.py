class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(...)
        pygame.display.set_caption(...)
        self.clock = pygame.time.Clock()
        self.stats = GameStats()
        self.scoreboard = Scoreboard(self.screen, self.stats)
        self.ship = Ship(self.screen)
        self.player_bullets = []
        self.alien_bombs = []
        self.aliens = []
        self.fleet_direction = 1
        self.last_shot_time = 0
        self._create_fleet()
    def run_game(self):
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_player_bullets()
                self._update_aliens()
                self._alien_fire()
                self._update_alien_bombs()
            self._update_screen()
            self.clock.tick(settings.FPS)
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit() -> use pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
    def _check_keydown_events(self, event):
        if event.key in (pygame.K_RIGHT, pygame.K_d):
            self.ship.moving_right = True
        elif event.key in (pygame.K_LEFT, pygame.K_a):
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE and self.stats.game_active:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            pygame.quit(); sys.exit()
        elif event.key == pygame.K_r and not self.stats.game_active:
            self._restart_game()
    def _check_keyup_events(self, event):
        if event.key in (pygame.K_RIGHT, pygame.K_d):
            self.ship.moving_right = False
        elif event.key in (pygame.K_LEFT, pygame.K_a):
            self.ship.moving_left = False
    def _fire_bullet(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot_time >= settings.BULLET_COOLDOWN:
            self.last_shot_time = now
            bullet = Bullet(self.screen, self.ship.rect.centerx, self.ship.rect.top, 1)
            self.player_bullets.append(bullet)
    def _update_player_bullets(self):
        for bullet in self.player_bullets[:]:
            bullet.update()
            if bullet.is_off_screen():
                self.player_bullets.remove(bullet)
        self._check_bullet_alien_collisions()
    def _check_bullet_alien_collisions(self):
        for bullet in self.player_bullets[:]:
            for alien in self.aliens[:]:
                if bullet.rect.colliderect(alien.rect):
                    self.player_bullets.remove(bullet)
                    self.aliens.remove(alien)
                    self.stats.score += settings.POINTS_PER_ALIEN
                    if self.stats.score > self.stats.high_score:
                        self.stats.high_score = self.stats.score
                    break
        if not self.aliens:
            self.stats.victory = True
            self.stats.game_active = False
    def _create_fleet(self):
        total_width = settings.ALIEN_COLUMNS * (alien width + spacing)
        ...