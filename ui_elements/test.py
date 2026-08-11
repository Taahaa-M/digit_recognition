import pygame as pg
from drawingBoard import DrawingBoard

pg.init()

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

screen = pg.display
screen.set_caption("Drawing Board test")
surface = screen.set_mode(SCREEN_DIMENSIONS)
clock = pg.time.Clock()
pg.time.set_timer(30, 2000)


newDrawingBoard = DrawingBoard(
    surface, 400, 400, 4,
    DARK_GREY, LIGHT_GREY, WHITE, WHITE,
    12, (0, 0)
)

newDrawingBoard.setCenter(WIDTH//2, HEIGHT//2)
    
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == 30:
            pass
            #newButton.toggleAbility()

    surface.fill(BLACK)
    newDrawingBoard.updateDraw()

    screen.update()
    clock.tick(FPS)

pg.quit()
