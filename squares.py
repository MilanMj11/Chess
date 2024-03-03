import pygame
from constants import *

class Squares:
    def __init__(self):
        self.squareList = {} # { 1 : (Sq1, Cl1) , 2: (Sq2, Cl2) ... }
        self.numberOfSquares = NCOLS * NROWS
        self.createSquares()

    def createSquares(self):
        for i in range(NROWS):
            for j in range(NCOLS):
                squareNumber = i * NCOLS + j + 1
                if ( squareNumber + i ) % 2 == 0:
                    color = BROWN
                else:
                    color = CREAM

                squareRect = pygame.Rect(TILEWIDTH * j, TILEHEIGHT * i, TILEWIDTH * (j+1), TILEHEIGHT * (i+1))
                self.squareList[squareNumber] = squareRect, color
                # pygame.draw(squareRect)
