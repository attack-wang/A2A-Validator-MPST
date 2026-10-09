_FONT_CACHE = {}
def _get_font(size, bold=False):
    key = (size, bold)
    if key not in _FONT_CACHE:
        _FONT_CACHE[key] = pygame.font.SysFont("arial", size, bold=bold)
    return _FONT_CACHE[key]