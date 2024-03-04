import pygame
from constants import *
from squares import Squares


class Piece:
    def __init__(self, p_type, color, square = None):
        self.type = p_type
        self.square = square  # Square Position ( number 1 -> 64 )
        self.color = color
        self.points = None
        self.setPoints()
        self.onTable = True
        self.moveToSquare(square)
    def moveToSquare(self, square):
        if square != None:
            self.square.piece = None
            self.square = square
            square.piece = self
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

    def takeFromTable(self):
        self.onTable = False
        self.square.piece = None
        self.square = None

    def render(self, surf):
        if self.onTable == False:
            return

        image = pygame.image.load("assets/white_pawn.png").convert()

        if self.type == PAWN:
            if self.color == WHITE:
                image = pygame.image.load("assets/white_pawn.png").convert()
            else:
                image = pygame.image.load("assets/black_pawn.png").convert()

        if self.type == ROOK:
            if self.color == WHITE:
                image = pygame.image.load("assets/white_rook.png").convert()
            else:
                image = pygame.image.load("assets/black_rook.png").convert()

        if self.type == BISHOP:
            if self.color == WHITE:
                image = pygame.image.load("assets/white_bishop.png").convert()
            else:
                image = pygame.image.load("assets/black_bishop.png").convert()

        if self.type == KNIGHT:
            if self.color == WHITE:
                image = pygame.image.load("assets/white_knight.png").convert()
            else:
                image = pygame.image.load("assets/black_knight.png").convert()

        if self.type == QUEEN:
            if self.color == WHITE:
                image = pygame.image.load("assets/white_queen.png").convert()
            else:
                image = pygame.image.load("assets/black_queen.png").convert()

        if self.type == KING:
            if self.color == WHITE:
                image = pygame.image.load("assets/white_king.png").convert()
            else:
                image = pygame.image.load("assets/black_king.png").convert()

        image.set_colorkey((100, 100, 100))
        surf.blit(image, self.square.getScreenPosition())
        # pygame.draw.circle(surf, self.color, (self.square.getScreenPosition()[0] + TILEWIDTH / 2 , self.square.getScreenPosition()[1] + TILEHEIGHT / 2), TILEHEIGHT / 2)
