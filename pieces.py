import pygame
from constants import *
from squares import Squares

class Piece:
    def __init__(self, p_type, square, color):
        self.type = p_type
        self.square = square # Square Position ( number 1 -> 64 )
        self.color = color
        self.points = None
        self.setPoints()

    def setPoints(self):
        if self.type == PAWN:
            self.points = 1
        if self.type == KNIGHT or self.type == BISHOP:
            self.points = 3
        if self.type == ROOK:
            self.points = 5
        if self.type == QUEEN:
            self.points = 9
        if self.type == KING:
            self.points = 100
            # -> I don't think he has any evaluation of points

    def render(self, surf):
        pygame.draw.circle(surf, self.color, (self.square.getScreenPosition()[0] + TILEWIDTH / 2 , self.square.getScreenPosition()[1] + TILEHEIGHT / 2), TILEHEIGHT / 2)