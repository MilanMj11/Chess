import pygame
from constants import *
from squares import Squares

class Chess:
    def __init__(self):
        pieces = {}   # (Piece, Position (1->64))
        self.squares = Squares()

    def drawBoard(self, surf):
        for square in self.squares.squareList:
            pygame.draw.rect(surf,self.squares.squareList[square][1], self.squares.squareList[square][0])

    def update(self):
        pass

    def render(self, surf):
        self.drawBoard(surf)
