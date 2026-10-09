'''
ui.py
Small rendering helpers shared by the game: the dashed centre line,
the scoreboard and generic centred text, drawn on a tkinter canvas.
'''
from settings import (SCREEN_WIDTH, SCREEN_HEIGHT, LINE_COLOR, WHITE,
                      SCORE_FONT_SIZE)
FONT_FAMILY = "Helvetica"
def draw_text(canvas, text, size, color, center_x, center_y):
    '''Draw `text` centred on (center_x, center_y).'''
    canvas.create_text(int(center_x), int(center_y), text=text,
                       fill=color, font=(FONT_FAMILY, size, "bold"))
def draw_center_line(canvas):
    '''Draw the dashed vertical line that separates the two halves.'''
    dash_height = 15
    gap = 12
    x = SCREEN_WIDTH // 2 - 2
    y = 0
    while y < SCREEN_HEIGHT:
        canvas.create_rectangle(x, y, x + 4, y + dash_height,
                                fill=LINE_COLOR, outline="")
        y += dash_height + gap
def draw_scores(canvas, score_left, score_right):
    '''Render both players' scores at the top of their field half.'''
    draw_text(canvas, str(score_left), SCORE_FONT_SIZE, WHITE,
              SCREEN_WIDTH * 0.25, 55)
    draw_text(canvas, str(score_right), SCORE_FONT_SIZE, WHITE,
              SCREEN_WIDTH * 0.75, 55)