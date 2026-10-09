'''
ui.py
Small drawing helpers used by the Game class: the dashed centre line,
the scoreboard and generic centred text (menus, messages, etc.).
'''
import pygame
import settings
_score_font = None
_message_font = None
_small_font = None
def _get_fonts():
    '''Lazily create the fonts (pygame.font must be initialised first).'''
    global _score_font, _message_font, _small_font
    if _score_font is None:
        _score_font = pygame.font.Font(None, 72)
        _message_font = pygame.font.Font(None, 48)
        _small_font = pygame.font.Font(None, 30)
    return _score_font, _message_font, _small_font
def draw_center_line(surface):
    '''Draw the dashed vertical line that separates the two halves.'''
    dash_height = 15
    gap = 10
    x = settings.SCREEN_WIDTH // 2 - 2
    y = 0
    while y < settings.SCREEN_HEIGHT:
        pygame.draw.rect(surface, settings.COLOR_FOREGROUND, (x, y, 4, dash_height))
        y += dash_height + gap
def draw_score(surface, score_left, score_right):
    '''Draw both players' scores at the top of the playfield.'''
    score_font, _, _ = _get_fonts()
    left_text = score_font.render(str(score_left), True, settings.COLOR_PADDLE_LEFT)
    right_text = score_font.render(str(score_right), True, settings.COLOR_PADDLE_RIGHT)
    surface.blit(left_text, (settings.SCREEN_WIDTH * 0.25 - left_text.get_width() // 2, 20))
    surface.blit(right_text, (settings.SCREEN_WIDTH * 0.75 - right_text.get_width() // 2, 20))
def draw_centered_text(surface, text, size='message', color=settings.COLOR_TEXT, y_offset=0):
    '''
    Render a single line of text horizontally centred on the screen.
    size: 'score' | 'message' | 'small' selects the font size.
    y_offset: vertical offset from the middle of the screen.
    '''
    score_font, message_font, small_font = _get_fonts()
    fonts = {'score': score_font, 'message': message_font, 'small': small_font}
    font = fonts.get(size, message_font)
    text_surface = font.render(text, True, color)
    position = (settings.SCREEN_WIDTH // 2 - text_surface.get_width() // 2,
                settings.SCREEN_HEIGHT // 2 - text_surface.get_height() // 2 + y_offset)
    surface.blit(text_surface, position)
def draw_controls(surface):
    '''Draw the control hints in the bottom corners of the playfield.'''
    _, _, small_font = _get_fonts()
    left_hint = small_font.render('P1: W / S', True, settings.COLOR_TEXT)
    right_hint = small_font.render('P2: Up / Down arrows', True, settings.COLOR_TEXT)
    surface.blit(left_hint, (settings.PADDLE_MARGIN, settings.SCREEN_HEIGHT - 30))
    surface.blit(right_hint,
                 (settings.SCREEN_WIDTH - settings.PADDLE_MARGIN - right_hint.get_width(),
                  settings.SCREEN_HEIGHT - 30))