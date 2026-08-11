import pygame as pg
from pages.defaults.ui_elements.button import TextButton

pg.init()

class ListSelect:
    def __init__(self, values, surface, width, height, spacing,
                 bgColour, clickedColour, highlightColour,
                 textFont, fontSize, textColour,
                 pos, rectRadius, borderThickness, highlightThickness):
        if pg.font.SysFont(textFont, fontSize).render(max(values), True, textColour).get_rect().width > width - (2*(spacing + height//2)):
            print("Need greater width or smaller font size to fit largest element.")
        else:
            self.values = values
            self.pointer = 0
            self.maxPointer = len(self.values) - 1

            self.surface = surface
            self.displayValueRect = pg.Rect((pos[0] + height + spacing, pos[1]), (width - 2*(height//2), height))

            self.rightButton = TextButton(surface, self.incrementPointer, height, height,
                                      bgColour, clickedColour, highlightColour,
                                      ">", textFont, fontSize, textColour,
                                      (pos[0] + height + 2*spacing + self.displayValueRect.width, pos[1]),
                                      rectRadius, borderThickness, highlightThickness, True)
            self.leftButton = TextButton(surface, self.decrementPointer, height, height,
                                      bgColour, clickedColour, highlightColour,
                                      "<", textFont, fontSize, textColour,
                                     pos, rectRadius, borderThickness, highlightThickness, False, True)
            
            # dimension attributes
            self.pos = pos # top left of the widget
            self.width = width
            self.height = height
            self.center = self.displayValueRect.center
            self.top = self.displayValueRect.top
            self.bottom = self.displayValueRect.bottom
            self.right = self.rightButton.right
            self.left = self.leftButton.left

            self.bgColour = bgColour
            self.spacing = spacing
            
            self.textFont = pg.font.SysFont(textFont, fontSize)
            self.text = self.values[self.pointer]
            self.textColour = textColour
            self.textSurface = self.textFont.render(self.text, True, self.textColour)
            self.textRect = self.textSurface.get_rect()
            self.textRect.center = self.displayValueRect.center


    def incrementPointer(self):
        if self.pointer < self.maxPointer:
            self.pointer += 1


    def decrementPointer(self):
        if self.pointer > 0:
            self.pointer -= 1
    
    
    def update(self):
        self.updateText()
        pg.draw.rect(self.surface, self.bgColour, self.displayValueRect)
        self.surface.blit(self.textSurface, self.textRect)
        self.rightButton.update()
        self.leftButton.update()


    def updateDimensions(self):
        self.center = self.displayValueRect.center
        self.top = self.displayValueRect.top
        self.bottom = self.displayValueRect.bottom
        self.right = self.rightButton.right
        self.left = self.leftButton.left


    def updateText(self):
        self.text = self.values[self.pointer]
        self.textSurface = self.textFont.render(self.text, True, self.textColour)
        self.textRect = self.textSurface.get_rect()
        self.textRect.center = self.displayValueRect.center


    def setCenter(self, x, y):
        translateX, translateY = (x - self.displayValueRect.centerx), (y - self.displayValueRect.centery)
        self.displayValueRect.center = (x, y)
        self.textRect.center = self.displayValueRect.center
        self.rightButton.translate(translateX, translateY)
        self.leftButton.translate(translateX, translateY)


    def get(self):
        return self.values[self.pointer]
