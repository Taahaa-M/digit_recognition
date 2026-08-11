import pygame as pg
from functools import reduce

pg.init()

class ErrorBox(pg.Rect):
    def __init__(self, surface, pos,
                 font, fontSize,
                 *funcs, **colours):
        
        pg.Rect.__init__(self, pos, (0, 0))
        
        self.font = pg.font.SysFont(font, fontSize)
        self.surface = surface
        
        self.showAll = False

        if "good" in colours:
            self.showAll = True
            self.goodColour = colours["good"]

        self.badColour = colours["bad"]

        self.text = []

        if isinstance(funcs[0], tuple):
            self.funcs = funcs[0]
        else:
            self.funcs = funcs
        """
        these functions are validation functions
        each function will return a string and a boolean
        the string is the message displayed to the user
        if the message is good, indicated by the boolean,
        the message is displayed in goodColour
        else it is displayed in badColour
        """


    # Draw after updating
    def updateDraw(self):
        self.update()
        self.draw()

    # Update error text
    def update(self):
        self.text = []

        rectYPosOffset = 0
        results = []

        for func in self.funcs:
            results.append(func())
            
        for result in results:
            if result[1] is False or self.showAll is True:
                colour = self.goodColour if result[1] else self.badColour

                text = self.font.render(result[0], True, colour)

                textRect = text.get_rect()
                textRect.top = self.top + rectYPosOffset
                textRect.centerx = self.centerx

                self.text.append({
                    "surface": text,
                    "rect": textRect,
                })

                rectYPosOffset += textRect.height

        self._updateDimensions()

        return reduce(lambda x, y: x[1] or y[1], results)[1]


    # Update dimensions after text is updated
    def _updateDimensions(self):
        if self.text and self.text != "":
            self.height = self.text[-1]["rect"].bottom - self.text[0]["rect"].top
            """uses the difference between:
                the top of the first error
                and the bottom of the last error

            to determine the height of the error"""

            self.bottom = self.text[-1]["rect"].bottom  # uses the bottom of the last text to position the rect correctly
        else:
            self.height = 0


    # Draw error text without updating
    def draw(self):
        for text in self.text:
            self.surface.blit(text["surface"], text["rect"])


    def setCenter(self, x, y):
        self.center = (x, y)

