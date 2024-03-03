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
    def initChessPieces(self):
        self.pieces.append(Piece(ROOK,self.squares.squareList[0],BLACK))
        self.pieces.append(Piece(ROOK,self.squares.squareList[7],BLACK))
        self.pieces.append(Piece(ROOK,self.squares.squareList[56],WHITE))
        self.pieces.append(Piece(ROOK,self.squares.squareList[63],WHITE))

        self.pieces.append(Piece(KNIGHT,self.squares.squareList[1],BLACK))
        self.pieces.append(Piece(KNIGHT,self.squares.squareList[6],BLACK))
        self.pieces.append(Piece(KNIGHT,self.squares.squareList[57],WHITE))
        self.pieces.append(Piece(KNIGHT,self.squares.squareList[62],WHITE))

        self.pieces.append(Piece(BISHOP,self.squares.squareList[2],BLACK))
        self.pieces.append(Piece(BISHOP,self.squares.squareList[5],BLACK))
        self.pieces.append(Piece(BISHOP,self.squares.squareList[58],WHITE))
        self.pieces.append(Piece(BISHOP,self.squares.squareList[61],WHITE))

        self.pieces.append(Piece(QUEEN,self.squares.squareList[3],BLACK))
        self.pieces.append(Piece(QUEEN,self.squares.squareList[59],WHITE))

        self.pieces.append(Piece(KING,self.squares.squareList[4],BLACK))
        self.pieces.append(Piece(KING,self.squares.squareList[60],WHITE))

        for i in range(48,56):
            self.pieces.append(Piece(PAWN,self.squares.squareList[i],WHITE))

        for i in range(8,16):
            self.pieces.append(Piece(PAWN,self.squares.squareList[i],BLACK))
    def drawBoard(self, surf):
        self.squares.renderSquares(surf)

    def update(self):
        pass

    def render(self, surf):
        self.drawBoard(surf)
        for piece in self.pieces:
            piece.render(surf)
