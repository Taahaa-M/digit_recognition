import pygame as pg

pg.init()

class Button(pg.Rect):
    def __init__(self, surface, func, width, height,
                 bgColour, clickedColour, highlightColour,
                 label, labelColour,
                 pos, rectRadius, borderThickness, highlightThickness,
                 isRight = False, isLeft = False, isLabelLeftAligned = None):
        '''
        This class will be used to create instances of buttons in different 'pages' in my program.
        This is an abstract class and will only be inherited from for different types of default buttons.
        For example: with icons instead of text, and with default colours and values (border thickness etc.)
        '''
        pg.Rect.__init__(self, pos, (width, height))
        
        # Functionality
        self.func = func
        self.active = False # Button will be 'active' when it can be clicked, i.e. when it is hovered over by mouse
        self.pressed = False  # This value will be 'True' when the mouse is pressing down on the button
        self.released = False  # If mouse button has been released each time the mouse moves on the button
        self.enabled = True
        
        # Colours
        self.bgColour = bgColour
        self.previousBgColour = (0, 0, 0)
        self.highlightColour = highlightColour
        self.clickedColour = clickedColour
        self.labelColour = labelColour

        # Attributes needed for drawing
        self.surface = surface
        self.borderThickness = borderThickness
        self.highlighted = False
        self.pos = pos # top left of the button
        self.width = width
        self.height = height
        self.topRect = pg.Rect(pos, (width, height))  # The top rectangle will shrink when the button is hovered over
                                                      # revealing the self rectangle, which is in highlight colour
        self.topRect.inflate_ip(-self.borderThickness*2, -self.borderThickness*2)
        
        self.rectRadius = rectRadius  # Used for the rounding of button corners in drawing
        self.highlightThickness = highlightThickness  # This will set how much the top rectangle will shrink to control the
                                                      # thickness of the higlight border that is shown
        self.isRight = isRight  # these are boolean values used to determine whether the 
        self.isLeft = isLeft    # the buttons will have rounding on all corners or only left or right
        self.isLabelLeftAligned = isLabelLeftAligned

        self.spacing = 10
        self.label = pg.transform.scale(
            label,
            (
                self.topRect.width - self.spacing,
                self.topRect.height - self.spacing
                )
            )
        self.labelRect = self.label.get_rect()

        self.setLabelColour(labelColour, self.bgColour)
        self.positionLabel()


    def update(self):
        if self.enabled:
            topColour = self.bgColour
            bottomColour = self.highlightColour
            labelColour = self.labelColour
                    
            if self.collidepoint(pg.mouse.get_pos()):
                if not pg.mouse.get_pressed()[0]:  # mouse needs to be released
                    self.released = True
                    if self.pressed:
                        if self.enabled:
                            self.func()
                        self.pressed = False

                if pg.mouse.get_pressed()[0] and self.active and self.released:
                    self.pressed = True
                    
                if self.pressed:
                    topColour = self.clickedColour
                    labelColour = self.bgColour
                    
                self.active = True
                self.highlight()
            else:
                self.released = False
                self.active = False
                self.deHighlight()
                self.pressed = False
                    
            self.draw(bottomColour, topColour, labelColour)


    def positionLabel(self):
        if self.isLabelLeftAligned is None:
            self.labelRect.center = self.center
        elif self.isLabelLeftAligned:
            self.labelRect.centery = self.centery
            self.labelRect.left = self.left + abs(self.top - self.labelRect.top)
        elif self.isLabelLeftAligned is False:
            self.labelRect.centery = self.centery
            self.labelRect.right = self.right - abs(self.top - self.labelRect.top)
            

    def setLabelColour(self, colour, bgColour=(0, 0, 0, 0)):
        for x in range(self.label.get_width()):
            for y in range(self.label.get_height()):
                currentColour = self.label.get_at((x, y))
                if currentColour == self.previousBgColour:
                    self.label.set_at((x, y), bgColour)
                else:
                    colour.a = currentColour.a
                    self.label.set_at((x, y), colour)

        self.previousBgColour = bgColour
        

    def draw(self, bottomColour, topColour, labelColour):
        if self.enabled:
            self.setLabelColour(labelColour, topColour)
            self.previousBgColour = topColour
            """
            if self.isRight:
                pg.draw.rect(self.surface, bottomColour, self,
                             border_top_right_radius = self.rectRadius, border_bottom_right_radius = self.rectRadius)
                pg.draw.rect(self.surface, topColour, self.topRect,
                             border_top_right_radius = self.rectRadius, border_bottom_right_radius = self.rectRadius)
            elif self.isLeft:
                pg.draw.rect(self.surface, bottomColour, self,
                             border_top_left_radius = self.rectRadius, border_bottom_left_radius = self.rectRadius)
                pg.draw.rect(self.surface, topColour, self.topRect,
                             border_top_left_radius = self.rectRadius, border_bottom_left_radius = self.rectRadius)
            else:
                pg.draw.rect(self.surface, bottomColour, self, border_radius = self.rectRadius)
                pg.draw.rect(self.surface, topColour, self.topRect, border_radius = self.rectRadius)
            """

            pg.draw.rect(self.surface, bottomColour, self)
            pg.draw.rect(self.surface, topColour, self.topRect)
    
            
            self.surface.blit(self.label, self.labelRect)
            

    def highlight(self):
        if self.highlighted == False:
            pg.Rect.inflate_ip(self.labelRect, -self.highlightThickness*2, -self.highlightThickness*2)
            self.positionLabel()
            self.topRect.inflate_ip(-self.highlightThickness*2, -self.highlightThickness*2)
            self.highlighted = True


    def deHighlight(self):
        if self.highlighted:
            self.label = pg.transform.scale(
            self.label,
            (
                self.labelRect.width + self.highlightThickness*2,
                self.labelRect.height + self.highlightThickness*2
                )
            )
            self.labelRect = self.label.get_rect()
            self.positionLabel()
            self.topRect.inflate_ip(self.highlightThickness*2, self.highlightThickness*2)
            self.highlighted = False


    def setCenter(self, x, y):
        self.center = (x, y)
        self.topRect.center = self.center
        self.positionLabel()


    def translate(self, dx, dy):
        self.x += dx
        self.y += dy
        self.topRect.center = self.center
        self.positionLabel()
        

    def enable(self):
        self.enabled = True
        

    def disable(self):
        self.enabled = False


    def toggleAbility(self):
        self.enabled = not self.enabled
        
        
class TextButton(Button):
    def __init__(self, surface, func, width, height,
                     bgColour, clickedColour, highlightColour,
                     text, font, fontSize, textColour,
                     pos, rectRadius, borderThickness, highlightThickness,
                     isRight = False, isLeft = False, isTextLeftAligned = None):
        self.text = text
        self.font = pg.font.SysFont(font, fontSize)
        label = self.font.render(self.text, True, textColour)
        
        Button.__init__(self, surface, func, width, height,
                     bgColour, clickedColour, highlightColour,
                     label, textColour,
                     pos, rectRadius, borderThickness, highlightThickness,
                     isRight, isLeft, isTextLeftAligned)
        

    def setLabelColour(self, colour, bgColour=None):
        self.label = self.font.render(self.text, True, colour)
        self.labelRect = self.label.get_rect()
        self.positionLabel()
