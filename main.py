import pygame as pg
from gui import SCREEN_DIMENSIONS, BLACK, FPS, DefaultButton, DefaultDrawingBoard
from model import Model

model = Model.load_model("mnist_sigmoid_model.npz")

screen = pg.display
screen.set_caption("Digit Recognition")
surface = screen.set_mode(SCREEN_DIMENSIONS)
clock = pg.time.Clock()

drawingBoard = DefaultDrawingBoard(surface)
button = DefaultButton(surface, "Guess", guess)

def main():
    running = True
    while running == True:
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                running = False

        surface.fill(BLACK)
        drawingBoard.updateDraw()
        button.update()

        screen.update()
        clock.tick(FPS)

    pg.quit()


def guess():
    print("Hello")


if __name__ == "__main__":
    main()
