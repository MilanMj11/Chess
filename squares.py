import pygame
from constants import *

class Square:
    def __init__(self, number):
        self.number = number
        self.rectangle = None
        self.setRectangle()
        self.color = None
        self.setColor()

    def getScreenPosition(self):
        line = (self.number - 1) // NCOLS
        col = (self.number - 1) % NROWS
        return (col * TILEWIDTH, line * TILEHEIGHT)
    def setRectangle(self):
        line = (self.number - 1) // NCOLS
        col = (self.number - 1) % NROWS
        self.rectangle = pygame.Rect(col * TILEWIDTH, line * TILEHEIGHT, (col+1) * TILEWIDTH, (line+1) * TILEHEIGHT)

    def setColor(self):
        if ( self.number + (self.number - 1) // NCOLS ) % 2 == 0:
            self.color = BROWN
        else:
            self.color = CREAM

    def render(self, surf):
        pygame.draw.rect(surf,self.color,self.rectangle)

class Squares:
    def __init__(self):
        self.squareList = []
        self.numberOfSquares = NCOLS * NROWS
        self.createSquares()

    def createSquares(self):
        for i in range(1,self.numberOfSquares + 1):
            self.squareList.append(Square(i))

    def renderSquares(self, surf):
        for square in self.squareList:
            square.render(surf)
