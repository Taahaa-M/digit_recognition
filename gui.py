import pygame as pg

from ui_elements.button import TextButton
from ui_elements.drawingBoard import DrawingBoard

pg.init()
pg.font.init()

BLACK = pg.Color(0, 0, 0)
GREEN = pg.Color(0, 255, 0)
RED = pg.Color(255, 0, 0)
WHITE = pg.Color(255, 255, 255)
LIGHT_GREY = pg.Color(220, 220, 220)
GREY = pg.Color(130, 130, 130)
DARK_GREY = pg.Color(70, 70, 70)
THE_COLOUR = pg.Color(96, 128, 160)
WIDTH, HEIGHT = 800, 450
SCREEN_DIMENSIONS = (WIDTH, HEIGHT)
FPS = 240


class DefaultDrawingBoard(DrawingBoard):
    def __init__(self, surface):
        DrawingBoard.__init__(self,
            surface, 400, 400, 4,
            DARK_GREY, LIGHT_GREY, WHITE, WHITE,
            12, (0, 0)
        )

        self.setCenter(WIDTH//2, HEIGHT//2)


class DefaultButton(TextButton):
    def __init__(self, surface, text, func):
        TextButton.__init__(self,
            surface, func,
            400, 100,
            DARK_GREY, LIGHT_GREY, WHITE,
            text, "Arial", 12, WHITE,
            (0, 0), 4, 2, 4
        )

        self.setCenter(WIDTH//2, HEIGHT//2)


screen = pg.display
screen.set_caption("Digit Recognition")
surface = screen.set_mode(SCREEN_DIMENSIONS)
clock = pg.time.Clock()
