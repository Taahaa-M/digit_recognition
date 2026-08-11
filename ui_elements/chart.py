import pygame as pg
from math import log10, trunc

pg.init()

class Chart(pg.Rect):
    def __init__(self, surface, width, height, pos,
                 axesThickness, axesColour,
                 dataPointColour, dataPointRadius,
                 lineColour, lineThickness,
                 labelSpacing, graphSpacing,
                 textColour, font, fontSize, divisionsFontSize,
                 yAxisName, xAxisName, xDivisions, yDivisions, significantFigs,
                 data, showXAxis = True):
        pg.Rect.__init__(self, pos, (width, height))
        # this rect is of the graphing area only, not including axes and labels
        
        # Drawing Attributes
        self.surface = surface
        self.axesColour = axesColour
        self.dataPointColour = dataPointColour
        self.lineColour = lineColour
        self.lineThickness = lineThickness
        self.font = pg.font.SysFont(font, fontSize)
        self.divisionsFont = pg.font.SysFont(font, divisionsFontSize)
        self.textColour = textColour
        self.labelSpacing = labelSpacing
        self.graphSpacing = graphSpacing

        # X-Axis
        self.xAxisRect = pg.Rect(self.left, self.bottom, self.width, axesThickness)
        
        # Y-Axis
        self.yAxisRect = pg.Rect(self.left - axesThickness, self.top, axesThickness, self.height + axesThickness)

        # Data
        self.data = data  # this is a 2D list, where each item is [xValue, yValue]
                          # a tuple of (xValue, yValue) could also be used
        self.dataPointRadius = dataPointRadius
        self.significantFigs = significantFigs
        self.xDivisions = xDivisions
        self.yDivisions = yDivisions
        self.dataCirclesCenters = []
        self.divisionLabels = []
        self.convertDataPointsToCoords()

        # X-Axis Label
        self.showXAxis = showXAxis
        self.xAxisName = xAxisName
        self.xLabelSurface = self.font.render(xAxisName, True, textColour)
        self.xLabelRect = self.xLabelSurface.get_rect()
        self.xLabelRect.centerx = self.xAxisRect.centerx
        if self.showXAxis:
            self.xLabelRect.top = self.divisionLabels[0][0][1].bottom + self.labelSpacing
        else:
            self.xLabelRect.top = self.bottom + self.xAxisRect.height + self.labelSpacing

        # Y-Axis Label
        self.yAxisName = yAxisName
        self.yLabelSurface = self.font.render(yAxisName, True, textColour)
        self.yLabelSurface = pg.transform.rotate(self.yLabelSurface, 90)
        self.yLabelRect = self.yLabelSurface.get_rect()
        self.yLabelRect.centery = self.yAxisRect.centery
        self.yLabelRect.right = (self.divisionLabels[1][0][1].centerx - self.labelSpacing - self.maxYLabelWidth//2)

        # Create entire graph rect
        self.wholeGraphRect = pg.Rect(self.yLabelRect.left,
                                     self.top,
                                     self.xAxisRect.right - self.yLabelRect.left,
                                     self.xLabelRect.bottom - self.yAxisRect.top)

        
    # Convert values into (x, y) coordinates that can be plotted on the graph
    def convertDataPointsToCoords(self):
        self.data.sort(key = lambda x: x[0])
        self.maxX = self.data[-1][0]
        self.maxY = max([dataPoint[1] for dataPoint in self.data])
        self.minX = self.data[0][0]
        self.minY = min([dataPoint[1] for dataPoint in self.data])
        
        self.rangeX = self.maxX - self.minX
        self.rangeY = self.maxY - self.minY

        self.convertLabelValuesToLabels()
        
        quotientX = (self.width - 2*self.graphSpacing)/self.rangeX
        quotientY = (self.height - 2*self.graphSpacing)/self.rangeY

        self.dataCirclesCenters = list(
            map(
                lambda dataPoint: (
                    round(self.x + self.graphSpacing + (dataPoint[0]-self.minX)*quotientX),
                    round(self.y - self.graphSpacing + self.height - (dataPoint[1]-self.minY)*quotientY)
                    ),
                self.data
                )
            )


    def convertLabelValuesToLabels(self):
        self.divisionLabels = []
        stepX = self.rangeX/self.xDivisions  # these are the intervals that the divisions will increase in
        stepY = self.rangeY/self.yDivisions

        xLabelValues = [self.minX + stepX*n for n in range(self.xDivisions + 1)]
        yLabelValues = [self.minY + stepY*n for n in range(self.yDivisions + 1)]
        self.maxXLabelWidth = 0
        self.maxYLabelWidth = 0

        # Create X Labels
        self.divisionLabels.append([])

        for labelValue in xLabelValues:
            labelValue = self.getValueString(labelValue)
            labelSurface = self.divisionsFont.render(labelValue, True, self.textColour)
            labelRect = labelSurface.get_rect()
            if labelRect.width > self.maxXLabelWidth:
                self.maxXLabelWidth = labelRect.width
                
            self.divisionLabels[0].append((labelSurface, labelRect))

        # Create Y Labels
        self.divisionLabels.append([])
        
        for labelValue in yLabelValues:
            labelValue = self.getValueString(labelValue)
            labelSurface = self.divisionsFont.render(labelValue, True, self.textColour)
            labelRect = labelSurface.get_rect()
            if labelRect.width > self.maxYLabelWidth:
                self.maxYLabelWidth = labelRect.width
            self.divisionLabels[1].append((labelSurface, labelRect))

        # Position X Labels
        xCenterYPos = self.xAxisRect.bottom + self.labelSpacing + self.divisionLabels[0][0][1].height//2
        stepX = (self.width - 2*self.graphSpacing)/self.xDivisions
        for i, label in enumerate(self.divisionLabels[0]):
            label[1].centerx = self.left + self.graphSpacing + i*stepX
            label[1].centery = xCenterYPos

        # Position Y Labels
        yCenterXPos = self.yAxisRect.left - self.labelSpacing - self.maxYLabelWidth//2
        stepY = (self.height - 2*self.graphSpacing)/self.yDivisions
        for i, label in enumerate(self.divisionLabels[1]):
            label[1].centerx = yCenterXPos
            label[1].centery = self.bottom - self.graphSpacing - i*stepY


    # Get a string of the value in the correct significant figures
    def getValueString(self, value):
        if value == 0:
            if self.significantFigs == 1:
                return "0"
            else:
                return "0." + (self.significantFigs - 1)*"0"
            
        value = str(round(value, self.getValueAccuracy(value)))

        fraction = False  # used to know when the values are now representing decimals
        significant = False
        significantCount = 0
        
        for i, char in enumerate(value):
            if char not in ("0", "-", "."):
                significant = True
                significantCount += 1
                
            elif char == "0" and significant:
                significantCount += 1

            elif char == ".":
                fraction = True

            if significantCount == self.significantFigs:
                if fraction:
                    return value[:i+1]  # returns entire string upto and including char at pointer i
                else:
                    return value[:-2]  # removes '.0' of float

        return value + (self.significantFigs - significantCount)*"0"  # adds 0s to meet sf requirement
            
            
    def getValueAccuracy(self, value):
        if value == 0:
            return self.significantFigs - 1
        
        numDigits = trunc(log10(abs(value))) + 1

        return self.significantFigs - numDigits


    # Draw the graph
    def draw(self):
        # Draw data points
        for i, dataPoint in enumerate(self.dataCirclesCenters):
            if i != len(self.data) - 1:
                pg.draw.line(self.surface, self.lineColour,
                             dataPoint, self.dataCirclesCenters[i+1],
                             width = self.lineThickness
                             )
            pg.draw.circle(self.surface, self.dataPointColour, dataPoint, self.dataPointRadius)

        # Draw  X division labels
        if self.showXAxis:
            for label in self.divisionLabels[0]:
                self.surface.blit(label[0], label[1])

        # Draw Y Division labels
        for label in self.divisionLabels[1]:
            self.surface.blit(label[0], label[1])
                
        pg.draw.rect(self.surface, self.axesColour, self.xAxisRect)
        pg.draw.rect(self.surface, self.axesColour, self.yAxisRect)
        self.surface.blit(self.xLabelSurface, self.xLabelRect)
        self.surface.blit(self.yLabelSurface, self.yLabelRect)


    def updateData(self, newData, xAxisName=None, yAxisName=None):
        if xAxisName is not None and xAxisName != self.xAxisName:
            self.xAxisName = xAxisName
            self.xLabelSurface = self.font.render(xAxisName, True, self.textColour)
            self.xLabelRect = self.xLabelSurface.get_rect()
            self.xLabelRect.centerx = self.xAxisRect.centerx

        if yAxisName is not None and yAxisName != self.yAxisName:
            self.yAxisName = yAxisName
            self.yLabelSurface = self.font.render(yAxisName, True, self.textColour)
            self.yLabelSurface = pg.transform.rotate(self.yLabelSurface, 90)
            self.yLabelRect = self.yLabelSurface.get_rect()

        if newData != self.data:
            self.data = newData
            self.convertDataPointsToCoords()

            # X-Axis Labels
            if self.showXAxis:
                self.xLabelRect.top = self.divisionLabels[0][0][1].bottom + self.labelSpacing
            else:
                self.xLabelRect.top = self.xAxisRect.bottom + self.labelSpacing

            # Y-Axis Label
            self.yLabelRect.right = (self.divisionLabels[1][0][1].centerx - self.labelSpacing - self.maxYLabelWidth//2)
            self.yLabelRect.centery = self.centery

            self.wholeGraphRect = pg.Rect(self.yLabelRect.left,
                                     self.top,
                                     self.xAxisRect.right - self.yLabelRect.left,
                                     self.yAxisRect.top - self.xLabelRect.bottom)
            

    def setCenter(self, pos, wholeGraph=False):
        # Calculate how much to move each element
        if wholeGraph:
            translateX, translateY = (pos[0] - self.wholeGraphRect.centerx, pos[1] - self.wholeGraphRect.centery)
        else:
            translateX, translateY = (pos[0] - self.centerx, pos[1] - self.centery)

        self.move_ip(translateX, translateY)
        self.wholeGraphRect.move_ip(translateX, translateY)
        
        self.xAxisRect.move_ip(translateX, translateY)
        self.yAxisRect.move_ip(translateX, translateY)
        
        self.xLabelRect.move_ip(translateX, translateY)
        self.yLabelRect.move_ip(translateX, translateY)

        for i in range(len(self.dataCirclesCenters)):
            self.dataCirclesCenters[i] = (
                self.dataCirclesCenters[i][0] + translateX,
                self.dataCirclesCenters[i][1] + translateY
                )

        for axis in self.divisionLabels:
            for label in axis:
                label[1].x += translateX
                label[1].y += translateY
