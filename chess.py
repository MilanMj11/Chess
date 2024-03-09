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

    def unselectEverything(self):
        for piece in self.pieces:
            piece.setCorrectPosition()
        for square in self.squares.squareList:
            square.setCorrectColor()

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

    def showPseudoLegalMoves(self):
        if self.selectedPiece != None:
            if (self.selectedPiece.color == WHITE and self.turn == WHITE_TURN) or (
                    self.selectedPiece.color == BLACK and self.turn == BLACK_TURN):
                for legalSquare in self.selectedPiece.legalMovesSquares():
                    legalSquare.changeRedColor()

    def holdingClick(self, mouse_pos, holding):

        if mouse_pos == None:
            return

        clickedSquare = self.squares.squareList[((mouse_pos[1] // TILEHEIGHT) * NCOLS + (mouse_pos[0] // TILEWIDTH))]

        if holding == False:
            if clickedSquare.piece != None:
                clickedSquare.piece.setCorrectPosition()
            return

        # If I'm holding click on a piece
        if clickedSquare.piece != None:
            if (clickedSquare.piece.color == WHITE and self.turn == WHITE_TURN) or (
                    clickedSquare.piece.color == BLACK and self.turn == BLACK_TURN):
                clickedSquare.piece.imagePosition = (
                    pygame.mouse.get_pos()[0] - TILEWIDTH / 2, pygame.mouse.get_pos()[1] - TILEHEIGHT / 2)

    def handleClick(self, mouse_pos, clickButton):
        # click can do 2 diff things : One when we have a selected piece already , and the other is just selecting.

        # I want to get the square that I clicked on

        clickedSquare = self.squares.squareList[((mouse_pos[1] // TILEHEIGHT) * NCOLS + (mouse_pos[0] // TILEWIDTH))]

        if clickButton == RIGHT_CLICK:

            if self.selectedPiece != None:
                self.selectedPiece.setCorrectPosition()
            if self.selectedSquare != None:
                self.unselectSquare()

            self.squares.resetBoardColor()
            return

        if self.selectedPiece != None:
            self.selectedPiece.setCorrectPosition()

        if self.selectedSquare == None and clickButton == LEFT_CLICK_PRESS:
            # If there was no selected square before this:

            # select the clicked square
            self.selectSquare(clickedSquare)

            # if it has a piece, show the PseudoLegalMoves
            if clickedSquare.piece != None:
                self.showPseudoLegalMoves()

            return

        if self.selectedSquare != None:

            if self.selectedSquare == clickedSquare:
                # self.unselectSquare()
                # self.squares.resetBoardColor()
                return

            # If there was a selected square before, I have more situations:

            # If the selected square has a piece :
            if self.selectedPiece != None:

                # If the previously selected piece was not the good color, act like it was just a square
                if not ((self.selectedPiece.color == WHITE and self.turn == WHITE_TURN) or (
                        self.selectedPiece.color == BLACK and self.turn == BLACK_TURN)):
                    self.unselectSquare()
                    self.squares.resetBoardColor()
                    # if the newly selected square has a piece that CAN move , I want to show the pseudo legal moves
                    if clickButton == LEFT_CLICK_PRESS:
                        self.selectSquare(clickedSquare)
                        self.showPseudoLegalMoves()
                    # self.showPseudoLegalMoves()
                    return
                # If the clicked square is a pseudoleagal position for the selected piece
                if clickedSquare in self.selectedPiece.legalMovesSquares():
                    # move to square ( capture square )

                    '''
                    ! CASTLE SITUATION !
                    '''
                    if self.selectedPiece.type == KING:
                        # print("OK")
                        if abs(clickedSquare.number - self.selectedPiece.square.number) == 2:
                            # print("BETTER")
                            if clickedSquare.number > self.selectedPiece.square.number:
                                rook = self.squares.squareList[clickedSquare.number].piece
                                rook.moveToSquare(self.squares.squareList[clickedSquare.number - 2])

                            if clickedSquare.number < self.selectedPiece.square.number:
                                rook = self.squares.squareList[clickedSquare.number - 3].piece
                                rook.moveToSquare(self.squares.squareList[clickedSquare.number])

                    self.selectedPiece.moveToSquare(clickedSquare)
                    # change turns because a move was done
                    if self.turn == WHITE_TURN:
                        self.turn = BLACK_TURN
                    else:
                        self.turn = WHITE_TURN
                    # unselect the previous square and reset all the colors
                    self.unselectSquare()
                    self.squares.resetBoardColor()
                # If the clicked square is not a pseudolegal position for the selected piece
                else:
                    # If the newly selected square is also a piece that we can move then select that instead
                    if clickedSquare.piece != None and clickButton == LEFT_CLICK_PRESS:
                        if (clickedSquare.piece.color == WHITE and self.turn == WHITE_TURN) or (
                                clickedSquare.piece.color == BLACK and self.turn == BLACK_TURN):
                            self.unselectSquare()
                            self.squares.resetBoardColor()
                            self.selectSquare(clickedSquare)
                            self.showPseudoLegalMoves()
                        else:
                            self.unselectSquare()
                            self.squares.resetBoardColor()
                            self.selectSquare(clickedSquare)
                    if clickedSquare.piece != None and clickButton == LEFT_CLICK_RELEASE:
                        self.unselectSquare()
                        self.squares.resetBoardColor()
                    if clickedSquare.piece == None:
                        self.unselectSquare()
                        self.squares.resetBoardColor()
                        '''
                        ! CHANGED !
                        '''
                        # self.selectSquare(clickedSquare)

                return
            # If the selected square does NOT have a piece
            if self.selectedPiece == None:
                self.unselectSquare()
                self.squares.resetBoardColor()

                # If the newly clicked square also does not have a piece:
                if clickedSquare.piece == None and clickButton == LEFT_CLICK_PRESS:
                    self.selectSquare(clickedSquare)

                # If the newly clicked square HAS a piece:
                if clickedSquare.piece != None and clickButton == LEFT_CLICK_PRESS:
                    self.selectSquare(clickedSquare)
                    if (clickedSquare.piece.color == WHITE and self.turn == WHITE_TURN) or (
                            clickedSquare.piece.color == BLACK and self.turn == BLACK_TURN):
                        self.showPseudoLegalMoves()

                return

            # self.squares.resetBoardColor()

    def update(self):
        pass

    def render(self, surf):
        self.drawBoard(surf)
        for piece in self.pieces:
            piece.render(surf)
