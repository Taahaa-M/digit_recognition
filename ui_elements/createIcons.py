import pygame as pg
from math import sin, cos, pi

pg.init()


BLACK = pg.Color(0, 0, 0)
GREEN = pg.Color(0, 255, 0)
RED = pg.Color(255, 0, 0)
WHITE = pg.Color(255, 255, 255)
LIGHT_GREY = pg.Color(220, 220, 220)
GREY = pg.Color(130, 130, 130)
DARK_GREY = pg.Color(70, 70, 70)
THE_COLOUR = pg.Color(96, 128, 160)
WIDTH, HEIGHT = 360, 360
SCREEN_DIMENSIONS = (WIDTH, HEIGHT)
FPS = 30

screen = pg.display
screen.set_caption("Button test")
surface = screen.set_mode(SCREEN_DIMENSIONS, 32)

colour = WHITE

polygonCount = 6
circleRadius = 60
centreCircleRadius = 64
angle = 2*pi/polygonCount
screenRect = surface.get_rect()
maxHeight = 320
circleDistance = 164

if polygonCount % 2 == 0:
    lineLength = maxHeight / 2
else:
    maxHeightLineNo = polygonCount // 2
    maxAngle = pi - maxHeightLineNo*angle
    # solve {x + xcos(maxAngle) = self.height} -> {x(1 + cos(maxAngle)) = self.height}
    # {x = self.height/(1 + cos(maxAngle)}
    lineLength = maxHeight/(1.0001 + cos(maxAngle))  # a small value is added to avoid a zero error

verticesCoords = [
    (
        screenRect.centerx + round(lineLength*cos(i*angle)), 
        screenRect.centery + round(lineLength*sin(i*angle))
        ) for i in range(polygonCount)
    ]

circleCoords = [
    (
        screenRect.centerx + round(circleDistance*cos(i*angle)), 
        screenRect.centery + round(circleDistance*sin(i*angle))
        ) for i in range(polygonCount)
    ]

# Create background polygons
bgPolygons = [
    (
        screenRect.center,
        verticesCoords[i-1],
        verticesCoords[i]
        ) for i in range(polygonCount)
    ]

def drawSettingsIcon():
    surface.fill(BLACK)

    for polygon in bgPolygons:
        pg.draw.polygon(surface, colour, polygon)

    for circle in circleCoords:
        pg.draw.circle(surface, BLACK, circle, circleRadius)

    pg.draw.circle(surface, BLACK, screenRect.center, centreCircleRadius)

    screen.update()

def drawStatsIcon():
    width = 24
    space = 168*2
    halfSpace = space//2
    start = (screenRect.centerx - halfSpace, screenRect.centery + halfSpace)
    end = (screenRect.centerx + halfSpace, screenRect.centery + halfSpace)

    xAxisRect = pg.draw.line(surface, WHITE, start, end, width = width)

    start = (xAxisRect.left + xAxisRect.height//2, xAxisRect.top)
    end = (start[0], screenRect.centery - halfSpace)
    pg.draw.line(surface, WHITE, start, end, width = width)

    dataPointRadius = 24

    randomPoints = [
        (300, 78),
        (236, 200),
        (138, 164),
        (76, 280)
    ]

    for circle in randomPoints:
        pg.draw.circle(surface, WHITE, circle, dataPointRadius)

    pg.draw.lines(surface, WHITE, False, randomPoints, width = width)

    screen.update()

def drawTargetIcon():
    width = 24
    targetRadius = 120
    indent = 60
    circleDistance = targetRadius - indent
    lineLength = 100
    lineLocation = circleDistance + lineLength
    angle = pi/2

    coords = [
        ((
            screenRect.centerx + round(circleDistance*cos(i*angle)), 
            screenRect.centery + round(circleDistance*sin(i*angle))
            ),
        (
            screenRect.centerx + round(lineLocation*cos(i*angle)), 
            screenRect.centery + round(lineLocation*sin(i*angle))
            ))
        for i in range(4)
        ]

    surface.fill(BLACK)

    for coordStart, coordEnd in coords:
        pg.draw.line(surface, WHITE, coordStart, coordEnd, width = width)

    pg.draw.circle(surface, WHITE, screenRect.center, targetRadius, width=width)

    screen.flip()

running = True
while running:
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            running = False
            pg.quit()

    drawStatsIcon()
    pg.image.save(surface, 'assets/statsIcon.bmp')
