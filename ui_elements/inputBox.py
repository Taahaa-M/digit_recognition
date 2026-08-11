from pages.defaults.ui_elements.button import TextButton
import pygame as pg

class InputBox(TextButton):
    def __init__(self, surface, pos, width, height,
                 defaultText, maxCharacters,
                 activeBgColour, activeClickedColour, activeHighlightColour,
                 borderThickness, highlightThickness, rectRadius,
                 font, fontSize, activeTextColour,
                 passiveBgColour, passiveClickedColour, passiveHighlightColour, passiveTextColour,
                 isRight = False, isLeft = False, isTextLeftAligned = True):
        
        # My input box will work as two separate buttons that both toggle each other:
        # One will exist in the passive state, and the other (the self) in the active using an attribute 'passive'
        
        TextButton.__init__(self, surface, self.toggleActive, width, height,
                        activeBgColour, activeClickedColour, activeHighlightColour,
                        "", font, fontSize, activeTextColour,
                        pos, rectRadius, borderThickness, highlightThickness,
                        isRight, isLeft, isTextLeftAligned)

        self.passiveButton = TextButton(surface, self.toggleActive, width, height,
                                    passiveBgColour, passiveClickedColour, passiveHighlightColour,
                                    defaultText, font, fontSize, passiveTextColour,
                                    pos, rectRadius, borderThickness, highlightThickness,
                                    isRight, isLeft, isTextLeftAligned)
        
        self.disable()

        # Functionality
        self.inputActive = False
        self.defaultText = defaultText
        self.maxCharacters = maxCharacters
        
        # Drawing attributes
        self.surface = surface
        self.activeBgColour = activeBgColour
        self.activeClickedColour = activeClickedColour
        self.activeBorderColour = activeHighlightColour
        self.isRight = isRight
        self.isLeft = isLeft

        # Passive Drawing attributes
        self.passiveBgColour = passiveBgColour
        self.passiveClickedColour = passiveClickedColour
        self.passiveTextColour = passiveTextColour


    def toggleActive(self):
        if self.inputActive:
            self.deactivate()
        else:
            self.activate()


    def activate(self):
        self.enable()
        self.passiveButton.disable()
        self.inputActive = True
        

    def deactivate(self):
        self.disable()
        self.passiveButton.enable()
        self.inputActive = False


    def updateText(self, events):
        if self.inputActive:
            for event in events:
                if event.type == pg.MOUSEBUTTONUP and not self.collidepoint(event.pos):
                    self.deactivate()
                    
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_BACKSPACE:
                        if event.mod & pg.KMOD_CTRL:
                            self.text = ""
                            
                        else:
                            self.text = self.text[:-1]
                            
                    elif event.key == pg.K_RETURN:
                        self.deactivate()
                        
                    elif event.unicode != "" and len(self.text) <= self.maxCharacters - 1:
                        self.text += event.unicode
                        
        self.label = self.font.render(self.text, True, self.labelColour)

        if self.text == "":
            self.passiveButton.text = self.defaultText
            self.labelRect = self.passiveButton.label.get_rect()
            self.labelRect.center = self.topRect.center
        else:
            self.passiveButton.text = self.text

    def get(self):
        return self.text
    
    
    def setCenter(self, x, y):
        TextButton.setCenter(self, x, y)
        self.passiveButton.setCenter(x, y)


    def translate(self, dx, dy):
        TextButton.translate(self, dx, dy)
        self.passiveButton.translate(dx, dy)

        
    def update(self, events):
        self.updateText(events)
        TextButton.update(self)
        self.passiveButton.update()

if __name__ == "__main__":
    BLACK = pg.Color(0, 0, 0)
    WHITE = pg.Color(255, 255, 255)
    LIGHT_GREY = pg.Color(220, 220, 220)
    GREY = pg.Color(130, 130, 130)
    DARK_GREY = pg.Color(70, 70, 70)
    THE_COLOUR = pg.Color(96, 128, 160)
    WIDTH, HEIGHT = 800, 450
    SCREEN_DIMENSIONS = (WIDTH, HEIGHT)
    FPS = 30

    screen = pg.display
    screen.set_caption("Button test")
    surface = screen.set_mode(SCREEN_DIMENSIONS)
    clock = pg.time.Clock()
    pg.time.set_timer(30, 2000)

    newInputBox = InputBox(surface, (0, 0), 200, 40,
                           "Username", 24,
                           LIGHT_GREY, LIGHT_GREY, BLACK,
                           2, 2, 3,
                           "Arial", 18, GREY,
                           DARK_GREY, GREY, LIGHT_GREY, WHITE,
                           False, False)

    newInputBox.setCenter(WIDTH//2, HEIGHT//2)
        
    running = True
    while running:
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                running = False
            if event.type == 30:
                pass

        surface.fill(WHITE)
        newInputBox.update(events)

        screen.update()
        clock.tick(FPS)

    pg.quit()
