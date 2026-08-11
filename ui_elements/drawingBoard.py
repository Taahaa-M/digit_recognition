import pygame as pg
import numpy as np

pg.init()

class DrawingBoard(pg.Rect):
    # indices for self.colours
    BG = 0
    FG = 1
    ON = 1
    OFF = 0

    # indices for mouse buttons

    DRAW = 0
    ERASE = 2

    def __init__(self, surface, width, height, pFactor,
                 bgOnColour, bgOffColour,
                 fgOnColour, fgOffColour,
                 strokeThickness, pos):
        '''
        Rectangle widget used to draw greyscale pictures with a mouse
        '''

        pg.Rect.__init__(self, pos, (width, height))

        try:
            assert(width % pFactor == 0)
            assert(height % pFactor == 0)
        except:
            print("For drawing board functionality, width and height values must be an integer multiple of the pFactor")
            quit()
        
        # Functionality
        self.active = False # Button will be 'active' when it can be clicked, i.e. when it is hovered over by mouse
        self.pressed = False  # This value will be 'True' when the mouse is pressing down on the button
        self.released = False  # If mouse button has been released each time the mouse moves on the button
        self.enabled = True
        
        # Colours
        self.colours = [
            [bgOffColour, bgOnColour],
            [fgOffColour, fgOnColour]
        ]

        # Attributes needed for drawing
        self.surface = surface
        self.width = width
        self.height = height

        self.width = width
        self.height = height

        self.pFactor = pFactor

        self.pixelWidth = width // pFactor
        self.pixelHeight = height // pFactor

        self.strokeThickness = strokeThickness

        self.resetDrawing()  # set self.drawing to 0s


    def _update(self):
        pressedButtons = pg.mouse.get_pressed()
        mousePos = pg.mouse.get_pos()
        
        # only update drawing if a button is pressed
        if True not in pressedButtons: return

        # check mouse is within the x-axis bounds
        if mousePos[0] < self.left: return
        if mousePos[0] > self.right: return

        # check mouse is within the y-axis bounds
        if mousePos[1] < self.top: return
        if mousePos[1] > self.bottom: return

        relMousePos = (
            mousePos[0] - self.left,
            mousePos[1] - self.top
        )

        xDrawingIdx = relMousePos[0] // self.pFactor
        yDrawingIdx = relMousePos[1] // self.pFactor

        isErasing = pressedButtons[DrawingBoard.ERASE]
        isDrawing = pressedButtons[DrawingBoard.DRAW]

        # choose EITHER erasing or drawing; erasure is prioritised
        self._gaussianBlur(
            relMousePos,
            xDrawingIdx,
            yDrawingIdx,
            isErasing
        )


    def _gaussianBlur(self, relMousePos, xIdx, yIdx, isErase):
        minXIdx = max(0, xIdx - self.strokeThickness)
        maxXIdx = min(self.pixelWidth - 1, xIdx + self.strokeThickness)
        minYIdx = max(0, yIdx - self.strokeThickness)
        maxYIdx = min(self.pixelHeight - 1, yIdx + self.strokeThickness)

        pixelRelPos = (
            (relMousePos[0] % self.pFactor) / self.pFactor,
            (relMousePos[1] % self.pFactor) / self.pFactor
        )

        for i in range(minXIdx, maxXIdx + 1):
            for j in range(minYIdx, maxYIdx + 1):
                xDist = abs(pixelRelPos[0] - (i - xIdx))
                yDist = abs(pixelRelPos[1] - (j - yIdx))

                xDist += 0.5
                yDist += 0.5

                d = 2 * (xDist**2 + yDist**2)**(1/2)

                if d > self.strokeThickness:
                    continue

                if isErase:
                    self.drawing[i][j] = 0.0
                    continue
                
                self.drawing[i][j] = 1.0


    def _draw(self):
        isEnabled = DrawingBoard.ON if self.enabled else DrawingBoard.OFF

        fgColour = self.colours[DrawingBoard.FG][isEnabled]
        bgColour = self.colours[DrawingBoard.BG][isEnabled]

        rectToDraw = pg.Rect(self.topleft, (self.pFactor, self.pFactor))

        for i in range(self.pixelWidth):
            for j in range(self.pixelHeight):
                # linearly interpolate using: 0 <= x <= 1
                colour = bgColour.lerp(fgColour, self.drawing[i][j])

                pg.draw.rect(self.surface, colour, rectToDraw)
                rectToDraw.y += self.pFactor

            rectToDraw.y = self.y
            rectToDraw.x += self.pFactor


    def updateDraw(self):
        self._update()
        self._draw()


    def getDrawing(self):
        return self.drawing


    def resetDrawing(self):
        self.drawing = [
            [
                0.0 for _ in range(self.pixelHeight)
            ] for _ in range(self.pixelWidth)
        ]

        """
        # draw a checkerboard if you want vv
        self.drawing = [
            [
                (i + j) % 2 for i in range(self.pixelHeight)
            ] for j in range(self.pixelWidth)
        ]
        """


    def setCenter(self, x, y):
        self.center = (x, y)


    def translate(self, dx, dy):
        self.x += dx
        self.y += dy
        

    def enable(self):
        self.enabled = True
        

    def disable(self):
        self.enabled = False


    def toggleAbility(self):
        self.enabled = not self.enabled


    def setStrokeThickness(self, strokeThickness):
        self.strokeThickness = strokeThickness
