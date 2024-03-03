import pygame
from constants import *
from squares import Squares
from pieces import Piece

class Chess:
    def __init__(self):
        self.pieces = []   # (Piece)
        self.squares = Squares()
        self.turn = WHITE_TURN
        self.initChessPieces()
        self.selectedPiece = None
    def initChessPieces(self):

        self.pieces.append(Piece(ROOK,BLACK,self.squares.squareList[0]))
        self.pieces.append(Piece(ROOK,BLACK,self.squares.squareList[7]))
        self.pieces.append(Piece(ROOK,WHITE,self.squares.squareList[56]))
        self.pieces.append(Piece(ROOK,WHITE,self.squares.squareList[63]))

        self.pieces.append(Piece(KNIGHT,BLACK,self.squares.squareList[1]))
        self.pieces.append(Piece(KNIGHT,BLACK,self.squares.squareList[6]))
        self.pieces.append(Piece(KNIGHT,WHITE,self.squares.squareList[57]))
        self.pieces.append(Piece(KNIGHT,WHITE,self.squares.squareList[62]))

        self.pieces.append(Piece(BISHOP,BLACK,self.squares.squareList[2]))
        self.pieces.append(Piece(BISHOP,BLACK,self.squares.squareList[5]))
        self.pieces.append(Piece(BISHOP,WHITE,self.squares.squareList[58]))
        self.pieces.append(Piece(BISHOP,WHITE,self.squares.squareList[61]))

        self.pieces.append(Piece(QUEEN,BLACK,self.squares.squareList[3]))
        self.pieces.append(Piece(QUEEN,WHITE,self.squares.squareList[59]))

        self.pieces.append(Piece(KING,BLACK,self.squares.squareList[4]))
        self.pieces.append(Piece(KING,WHITE,self.squares.squareList[60]))

        for i in range(48,56):
            self.pieces.append(Piece(PAWN,WHITE,self.squares.squareList[i]))

        for i in range(8,16):
            self.pieces.append(Piece(PAWN,BLACK,self.squares.squareList[i]))


    def drawBoard(self, surf):
        self.squares.renderSquares(surf)


    def handleClick(self, mouse_pos):
        pass

    def update(self):
        pass

    def render(self, surf):
        self.drawBoard(surf)
        for piece in self.pieces:
            piece.render(surf)
