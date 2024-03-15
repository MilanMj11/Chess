import pygame
from constants import *

class Square:
    def __init__(self, number):
        self.number = number
        self.rectangle = None
        self.setRectangle()
        self.color = None
        self.setCorrectColor()
        self.piece = None

    def getScreenPosition(self):
        line = (self.number - 1) // NCOLS
        col = (self.number - 1) % NROWS
        return (col * TILEWIDTH, line * TILEHEIGHT)
    def setRectangle(self):
        line = (self.number - 1) // NCOLS
        col = (self.number - 1) % NROWS
        self.rectangle = pygame.Rect(col * TILEWIDTH, line * TILEHEIGHT, (col+1) * TILEWIDTH, (line+1) * TILEHEIGHT)

    def changeRedColor(self):
        if self.color == GREY:
            self.color = HARD_RED
        else:
            self.color = LIGHT_RED
    def changeColor(self, color):
        self.color = color
    def setCorrectColor(self):
        if ( self.number + (self.number - 1) // NCOLS ) % 2 == 0:
            self.color = BLUE
        else:
            self.color = GREY

    def render(self, surf):
        pygame.draw.rect(surf,self.color,self.rectangle)

class Squares:
    def __init__(self):
        self.squareList = []
        self.numberOfSquares = NCOLS * NROWS
        self.createSquares()

    def resetBoardColor(self):
        for square in self.squareList:
            square.setCorrectColor()
    def createSquares(self):
        for i in range(1,self.numberOfSquares + 1):
            self.squareList.append(Square(i))

    def renderSquares(self, surf):
        for square in self.squareList:
            square.render(surf)
