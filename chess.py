import pygame
from constants import *
from squares import Squares
from pieces import Piece


class Chess:
    def __init__(self):
        self.pieces = []  # (Piece)
        self.squares = Squares()
        self.turn = WHITE_TURN
        self.initChessPieces()
        self.selectedPiece = None
        self.selectedSquare = None

    def initChessPieces(self):

        self.pieces.append(Piece(self, ROOK, BLACK, self.squares.squareList[0]))
        self.pieces.append(Piece(self, ROOK, BLACK, self.squares.squareList[7]))
        self.pieces.append(Piece(self, ROOK, WHITE, self.squares.squareList[56]))
        self.pieces.append(Piece(self, ROOK, WHITE, self.squares.squareList[63]))

        self.pieces.append(Piece(self, KNIGHT, BLACK, self.squares.squareList[1]))
        self.pieces.append(Piece(self, KNIGHT, BLACK, self.squares.squareList[6]))
        self.pieces.append(Piece(self, KNIGHT, WHITE, self.squares.squareList[57]))
        self.pieces.append(Piece(self, KNIGHT, WHITE, self.squares.squareList[62]))

        self.pieces.append(Piece(self, BISHOP, BLACK, self.squares.squareList[2]))
        self.pieces.append(Piece(self, BISHOP, BLACK, self.squares.squareList[5]))
        self.pieces.append(Piece(self, BISHOP, WHITE, self.squares.squareList[58]))
        self.pieces.append(Piece(self, BISHOP, WHITE, self.squares.squareList[61]))

        self.pieces.append(Piece(self, QUEEN, BLACK, self.squares.squareList[3]))
        self.pieces.append(Piece(self, QUEEN, WHITE, self.squares.squareList[59]))

        self.pieces.append(Piece(self, KING, BLACK, self.squares.squareList[4]))
        self.pieces.append(Piece(self, KING, WHITE, self.squares.squareList[60]))

        for i in range(48, 56):
            self.pieces.append(Piece(self, PAWN, WHITE, self.squares.squareList[i]))

        for i in range(8, 16):
            self.pieces.append(Piece(self, PAWN, BLACK, self.squares.squareList[i]))

    def drawBoard(self, surf):
        self.squares.renderSquares(surf)

    def selectSquare(self, square):
        self.selectedSquare = square
        self.selectedSquare.changeRedColor()
        if square.piece != None:
            self.selectedPiece = square.piece

    def unselectSquare(self):
        self.selectedSquare.setCorrectColor()
        self.selectedSquare = None
        self.selectedPiece = None

    def handleClick(self, mouse_pos):
        # click can do 2 diff things : One when we have a selected piece already , and the other is just selecting.

        # I want to get the square that I clicked on

        clickedSquare = self.squares.squareList[((mouse_pos[1] // TILEHEIGHT) * NCOLS + (mouse_pos[0] // TILEWIDTH))]

        if self.selectedSquare == None:
            self.selectSquare(clickedSquare)
            if clickedSquare.piece != None:
                for legalSquare in clickedSquare.piece.legalMovesSquares():
                    # legalSquare.changeColor(RED)
                    legalSquare.changeRedColor();
        else:
            if clickedSquare == self.selectedSquare:
                self.unselectSquare()
                self.squares.resetBoardColor()
            else:
                if self.selectedPiece != None:
                    self.selectedPiece.moveToSquare(clickedSquare)
                    self.unselectSquare()
                    self.squares.resetBoardColor()
                else:
                    self.unselectSquare()
                    self.selectSquare(clickedSquare)

        '''
        self.selectedSquare = clickedSquare
        self.selectedSquare.changeColor(RED)
        if clickedSquare.piece != None:
            self.selectedPiece = clickedSquare.piece

        if self.selectedPiece != None:
            if self.selectedSquare != self.selectedPiece.square:
                self.selectedPiece.moveToSquare(self.selectedSquare)
                self.selectedSquare.setCorrectColor()
                self.selectedPiece = None
                self.selectedSquare = None
        '''

    def update(self):
        pass

    def render(self, surf):
        self.drawBoard(surf)
        for piece in self.pieces:
            piece.render(surf)
