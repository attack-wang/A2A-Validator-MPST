class SoundManager:
    def __init__(self):
        self.enabled = False
        try:
            pygame.mixer.pre_init(22050, -16, 1, 512)
            # actually pre_init must be called before pygame.init(); main.py will call pygame.init() first... 