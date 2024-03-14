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
        self.movesHistory = []  # (Piece, Square1, Square2)
        self.gameOver = None

    def positionEvaluation(self):
        # here I want to analyse the position for each color and give some results:

        # self.checkIfGameOver()
        if self.gameOver == True:
            if self.turn == WHITE_TURN:
                return [(10000, 0)]
            else:
                return [(0,10000)]

        # Material evaluation
        whiteValue = 0
        blackValue = 0

        # Piece development
        whiteDevelopment = 0
        blackDevelopment = 0

        # Centralization of pieces
        whiteCentralization = 0
        blackCentralization = 0

        for piece in self.pieces:
            if piece.onTable == True:
                if piece.color == WHITE:
                    whiteValue += piece.points * 100
                    whiteDevelopment += piece.hasMoved
                    whiteCentralization += piece.centralizationPoints()
                if piece.color == BLACK:
                    blackValue += piece.points * 100
                    blackDevelopment += piece.hasMoved
                    blackCentralization += piece.centralizationPoints()

        materialEvaluation = (whiteValue, blackValue)
        pieceDevelopment = (whiteDevelopment, blackDevelopment)
        pieceCentralization = (whiteCentralization, blackCentralization)

        #pieceDevelopment
        return [materialEvaluation, pieceCentralization, pieceDevelopment]

    def interpretEvaluation(self, list):
        score = 0
        for criteria in list:
            whiteScore = criteria[0]
            blackScore = criteria[1]
            score += (whiteScore - blackScore)
        return score

    def checkIfGameOver(self):
        available_moves = 0
        if self.turn == WHITE_TURN:
            for piece in self.pieces:
                if piece.onTable == True and piece.color == WHITE:
                    available_moves += len(piece.actualLegalMovesSquares())
        if self.turn == BLACK_TURN:
            for piece in self.pieces:
                if piece.onTable == True and piece.color == BLACK:
                    available_moves += len(piece.actualLegalMovesSquares())
        if available_moves == 0:
            if self.turn == WHITE_TURN:
                # print("NOT OK")
                if self.areKingsChecked()[0] == False:
                    # print("NOT AMAZING")
                    self.gameOver = DRAW
                    return
                self.gameOver = BLACK
            else:
                # print("OK")
                if self.areKingsChecked()[1] == False:
                    # print("PERFECT")
                    self.gameOver = DRAW
                    return
                self.gameOver = WHITE
        # print(available_moves)

    def getSquareByNumber(self, nr):
        for square in self.squares.squareList:
            if square.number == nr:
                return square
        return None

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
            if piece.onTable:
                piece.setCorrectPosition()
        for square in self.squares.squareList:
            square.setCorrectColor()

    def printMovesHistory(self):
        for move in self.movesHistory:
            print(move)

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

    def areKingsChecked(self):  # (whiteKingChecked , blackKingChecked)
        # check if black king is checked
        blackKing = None
        for piece in self.pieces:
            if piece.type == KING and piece.color == BLACK:
                blackKing = piece
                break
        if blackKing == None:
            return (-1, -1)
        blackKingChecked = False
        for piece in self.pieces:
            if piece.onTable == True and piece.color == WHITE:
                for square in piece.pseudoLegalMovesSquares():
                    if square == blackKing.square:
                        blackKingChecked = True
                        break

        # check if white king is checked
        whiteKing = None
        for piece in self.pieces:
            if piece.type == KING and piece.color == WHITE:
                whiteKing = piece
                break
        if whiteKing == None:
            return (-1, -1)
        whiteKingChecked = False
        for piece in self.pieces:
            if piece.onTable == True and piece.color == BLACK:
                for square in piece.pseudoLegalMovesSquares():
                    if square == whiteKing.square:
                        whiteKingChecked = True
                        break

        return (whiteKingChecked, blackKingChecked)

    def showActualLegalMoves(self):
        if self.selectedPiece != None:
            if (self.selectedPiece.color == WHITE and self.turn == WHITE_TURN) or (
                    self.selectedPiece.color == BLACK and self.turn == BLACK_TURN):
                for legalSquare in self.selectedPiece.actualLegalMovesSquares():
                    legalSquare.changeRedColor()

    def showPseudoLegalMoves(self):
        if self.selectedPiece != None:
            if (self.selectedPiece.color == WHITE and self.turn == WHITE_TURN) or (
                    self.selectedPiece.color == BLACK and self.turn == BLACK_TURN):
                for legalSquare in self.selectedPiece.pseudoLegalMovesSquares():
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
        # self.printMovesHistory()

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
                self.showActualLegalMoves()

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
                        self.showActualLegalMoves()
                    # self.showPseudoLegalMoves()
                    return
                # If the clicked square is a pseudoleagal position for the selected piece
                if clickedSquare in self.selectedPiece.actualLegalMovesSquares():
                    # move to square ( capture square )

                    '''
                    ! EN PASSANT SITUATION !
                    '''

                    if self.selectedPiece.type == PAWN:
                        # If I take diagonally , I want to check if I take to a square that is empty
                        if abs(clickedSquare.number - self.selectedPiece.square.number) == 7 or abs(
                                clickedSquare.number - self.selectedPiece.square.number) == 9:
                            if clickedSquare.piece == None:
                                # means that an en passant was commited:
                                if self.selectedPiece.color == WHITE:
                                    enPassantSquare = self.getSquareByNumber(clickedSquare.number + 8)
                                else:
                                    enPassantSquare = self.getSquareByNumber(clickedSquare.number - 8)
                                enPassantSquare.piece.takeFromTable()

                    '''
                    ! CASTLE SITUATION !
                    '''
                    castled = False

                    if self.selectedPiece.type == KING:
                        # print("OK")
                        if abs(clickedSquare.number - self.selectedPiece.square.number) == 2:
                            # print("BETTER")
                            if clickedSquare.number > self.selectedPiece.square.number:
                                rook = self.squares.squareList[clickedSquare.number].piece
                                rook.moveToSquare(self.squares.squareList[clickedSquare.number - 2])
                                self.movesHistory.append("Small Castle")
                                castled = True

                            if clickedSquare.number < self.selectedPiece.square.number:
                                rook = self.squares.squareList[clickedSquare.number - 3].piece
                                rook.moveToSquare(self.squares.squareList[clickedSquare.number])
                                self.movesHistory.append("Big Castle")
                                castled = True

                    if castled == False:
                        self.movesHistory.append((self.selectedPiece, self.selectedSquare, clickedSquare))

                    self.selectedPiece.moveToSquare(clickedSquare)

                    # change turns because a move was done
                    if self.turn == WHITE_TURN:
                        self.turn = BLACK_TURN
                    else:
                        self.turn = WHITE_TURN

                    self.checkIfGameOver()
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
                            self.showActualLegalMoves()
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
                        self.showActualLegalMoves()

                return

            # self.squares.resetBoardColor()

    def update(self):
        pass

    def render(self, surf):
        self.drawBoard(surf)
        for piece in self.pieces:
            piece.render(surf)
