import pygame as pg
from math import pi, cos, sin
from random import randint

pg.init()

class StatsPolygon(pg.Rect):
    def __init__(self, surface, pos, width,
                 bgColour, lineColour, statColour,
                 divisions, divisionLineLength, lineThickness,
                 font, fontSize, textColour,
                 labelSpacing, sizeDampening,
                 *stats, **kwargs):

        pg.Rect.__init__(self, pos, (width, width))

        self.surface = surface
        self.font = pg.font.SysFont(font, fontSize)
        self.textColour = textColour
        self.labelSpacing = labelSpacing

        self.statColour = statColour
        self.bgColour = bgColour

        self.lineColour = lineColour
        self.divisions = divisions
        self.divisionLineLength = divisionLineLength
        self.sizeDampening = sizeDampening
        self.lineThickness = lineThickness

        self.showBg = kwargs["showBg"]

        if isinstance(stats[0][0], tuple) or isinstance(stats[0][0], list):
            self.stats = stats[0][0]
        else:
            self.stats = stats
            
        self.calcPolyCoords()
        self.createLabels()

    # Function to update stats
    def updateData(self, *stats):
        if isinstance(stats[0][0], tuple) or isinstance(stats[0][0], list):
            self.stats = stats[0][0]
        else:
            self.stats = stats
            
        self.calcPolyCoords()
        self.createLabels()


    # Function to position by centre
    def setCenter(self, x, y):
        self.center = (x, y)
        self.calcPolyCoords()
        self.createLabels()


    # Function to draw self
    def draw(self):
        # Draw background polygon
        if self.showBg:
            for polygon in self.bgPolygons:
                pg.draw.polygon(self.surface, self.bgColour, polygon)

        # Draw stats polygon as calculated in calcPolyCoords
        for polygon in self.polygons:
            pg.draw.polygon(self.surface, self.statColour, polygon)

        # Draw lines from centre to ends of polygon
        for coord in self.verticesCoords:
            pg.draw.line(self.surface,
                         self.lineColour,
                         self.center,
                         coord
                         #, width=self.lineThickness
                         )

        # Draw division lines
        for coordSet in self.divisionsCoords:
            pg.draw.lines(self.surface,
                          self.lineColour,
                          True,
                          coordSet
                          #, width=self.lineThickness
                          )

        # Draw text
        for label, rect in self.labels:
            self.surface.blit(label, rect)


    # Function to calculate coordinates of polygons - a list of coordinate triplets
    def calcPolyCoords(self):
        polygonCount = len(self.stats)

        self.angle = 2*pi/polygonCount

        if polygonCount % 2 == 0:
            self.lineLength = self.height / 2
        else:
            maxHeightLineNo = polygonCount // 2
            maxAngle = pi - maxHeightLineNo*self.angle
            # solve {x + xcos(maxAngle) = self.height} -> {x(1 + cos(maxAngle)) = self.height}
            # {x = self.height/(1 + cos(maxAngle)}
            self.lineLength = self.height/(1.0001 + cos(maxAngle))  # a small value is added to avoid a zero error

        data = list(map(lambda x: x[1], self.stats))
        dampening = 1.2
        data = list(map(lambda x: x/(max(data)*dampening), data))

        self.dataPointsCoords = [
            (
                self.centerx + round(data[i]*self.lineLength*cos(i*self.angle - pi/2)), 
                self.centery + round(data[i]*self.lineLength*sin(i*self.angle - pi/2))
                ) for i in range(polygonCount)
            ]

        self.polygons = [
            (
                self.center,
                self.dataPointsCoords[i-1],
                self.dataPointsCoords[i]
                ) for i in range(polygonCount)
            ]

        # Create points for ends of background polygon
        # pi offset is to orient polygon correctly
        self.verticesCoords = [
            (
                self.centerx + round(self.lineLength*cos(i*self.angle - pi/2)), 
                self.centery + round(self.lineLength*sin(i*self.angle - pi/2))
                ) for i in range(len(self.stats))
            ]

        # Create background polygons
        self.bgPolygons = [
            (
                self.center,
                self.verticesCoords[i-1],
                self.verticesCoords[i]
                ) for i in range(polygonCount)
            ]

        # Create division line coordinates
        self.divisionsCoords = [
            [
                (
                    self.centerx + i*(coord[0] - self.centerx)/self.divisions,
                    self.centery + i*(coord[1] - self.centery)/self.divisions,
                    )
                for coord in self.verticesCoords
                ]
                for i in range(1, self.divisions + 1)
            ]


    # Function to create label surfaces and rects
    def createLabels(self):
        self.labels = []
        for i, label in enumerate(self.stats):
            labelText = self.font.render(label[0], True, self.textColour)
            labelRect = labelText.get_rect()

            if self.verticesCoords[i][0] > self.centerx:
               labelRect.left = self.verticesCoords[i][0] + self.labelSpacing
            elif self.verticesCoords[i][0] < self.centerx:
               labelRect.right = self.verticesCoords[i][0] - self.labelSpacing
            else:
               labelRect.centerx = self.centerx

            if self.verticesCoords[i][1] > self.centery:
               labelRect.top = self.verticesCoords[i][1] + self.labelSpacing
            elif self.verticesCoords[i][1] < self.centery:
               labelRect.bottom = self.verticesCoords[i][1] - self.labelSpacing
            else:
               labelRect.centery = self.centery

            self.labels.append((labelText, labelRect))


if __name__ == "__main__":
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
    FPS = 30

    screen = pg.display
    screen.set_caption("Button test")
    surface = screen.set_mode(SCREEN_DIMENSIONS, pg.DOUBLEBUF, 32)
    clock = pg.time.Clock()
    pg.time.set_timer(30, 500)

    spacing = 32
    newStatPolygon = StatsPolygon(surface, (WIDTH//2, HEIGHT//2), 200,
                                 LIGHT_GREY, GREY, THE_COLOUR, 4, 8, 2,
                                 "Arial", 12, WHITE, 12, 1.15,
                                 ("Righteousness", 7), ("Overshoot", 9), ("Accuracy", 6), ("Speed", 10), ("Bias", 4), ("Consistency", 8),
                                 showBg=False)


    running = True
    while running:
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                running = False
            if event.type == 30:
                newStatPolygon.setCenter(WIDTH//2 + randint(-20, 20), HEIGHT//2 + randint(-20, 20))

        surface.fill(BLACK)
        newStatPolygon.draw()

        screen.update()
        clock.tick(FPS)

    pg.quit()
