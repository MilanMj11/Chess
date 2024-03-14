import pygame
from constants import *
from squares import *

KNIGHT_OFFSET = [(2, 1), (1, 2), (-1, 2), (2, -1), (-2, 1), (1, -2), (-2, -1), (-1, -2)]
KING_OFFSET = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
BISHOP_OFFSET = [(1, 1), (-1, -1), (-1, 1), (1, -1)]
ROOK_OFFSET = [(1, 0), (0, 1), (-1, 0), (0, -1)]


class Piece:
    def __init__(self, chessGame, p_type, color, square=None):
        self.chessGame = chessGame
        self.type = p_type
        self.square = square  # Square Position ( number 1 -> 64 )
        self.color = color
        self.points = None
        self.setPoints()
        self.onTable = True
        self.moveToSquare(square)
        self.hasMoved = False
        self.position = self.getBoardPosition()
        self.image = None
        self.setImage()
        self.imagePosition = None
        self.setCorrectPosition()
        # self.Squares = Squares()

    def setCorrectPosition(self):
        self.imagePosition = self.square.getScreenPosition()

    def interior(self, position):
        if position[0] >= 0 and position[0] < NCOLS and position[1] >= 0 and position[1] < NROWS:
            return True
        return False

    def distanceFromSquare(self, squareNumber):
        linediff = abs((squareNumber - 1) // NCOLS - (self.square.number - 1) // NCOLS)
        coldiff = abs((squareNumber - 1) % NROWS - (self.square.number - 1) % NROWS)
        return linediff + coldiff

    def centralizationPoints(self):
        # I want to see how far from the center the square of the piece is
        # the center is : 28,29,36,37
        dist1 = self.distanceFromSquare(28)
        dist2 = self.distanceFromSquare(29)
        dist3 = self.distanceFromSquare(36)
        dist4 = self.distanceFromSquare(37)
        return -1 * ( dist1 + dist2 + dist3 + dist4 ) * (10 - self.points)

    def simulateMove(self, square):
        if square != None:
            squarePiece = None
            if square.piece != None:
                squarePiece = square.piece
                squarePiece.onTable = False
            self.square.piece = None
            prevSquare = self.square
            self.square = square
            square.piece = self
            if self.hasMoved == False:
                wasmoved = False
            else:
                wasmoved = True
            self.hasMoved = True
            changedType = False
            if self.type == PAWN and self.color == WHITE:
                if 1 <= square.number and square.number <= 8:
                    self.type = QUEEN
                    changedType = True

            if self.type == PAWN and self.color == BLACK:
                if 57 <= square.number and square.number <= 64:
                    self.type = QUEEN
                    changedType = True

            # self.chessGame.checkIfGameOver()

            return (prevSquare, squarePiece, wasmoved, changedType)

    def undoSimulatedMove(self, prevSquare, squarePiece, wasmoved, changedType):
        self.square.piece = None
        if squarePiece != None:
            squarePiece.onTable = True
            self.square.piece = squarePiece
        prevSquare.piece = self
        self.square = prevSquare
        if wasmoved == False:
            self.hasMoved = False
        if changedType == True:
            self.type = PAWN

        # if self.chessGame.gameOver == True:
           #  self.chessGame.gameOver = False

    # Returns a list of the squares that a piece can move to ( Pseudo legal moves )
    def actualLegalMovesSquares(self):
        # Take all pseudo legal moves
        legalSquareList = self.pseudoLegalMovesSquares()
        squaresToDelete = []
        # Now eliminate those that produce wrong behaviour
        for square in legalSquareList:

            # let's simulate I move the piece to that position and see bad behaviour
            ''' '''
            simulateInfo = self.simulateMove(square)
            KingsChecked = self.chessGame.areKingsChecked()
            # print(square.number, KingsChecked)
            if self.color == WHITE and KingsChecked[0] == True:
                # wrong behaviour , can't move
                squaresToDelete.append(square)
            if self.color == BLACK and KingsChecked[1] == True:
                # wrong behaviour , can't move
                squaresToDelete.append(square)

            # now I want to move it back:
            self.undoSimulatedMove(simulateInfo[0], simulateInfo[1], simulateInfo[2], simulateInfo[3])

        ''' castle situation with check '''

        if self.type == KING:
            for square in legalSquareList:
                if abs(self.square.number - square.number) == 2:
                    # we know the square in for is now the position for castle
                    # we want to get the square between the KING and the castle position
                    if square.number > self.square.number:
                        middleSquare = self.chessGame.getSquareByNumber(self.square.number + 1)
                    else:
                        middleSquare = self.chessGame.getSquareByNumber(self.square.number - 1)

                    if middleSquare in squaresToDelete:
                        squaresToDelete.append(square)

                    KingsChecked = self.chessGame.areKingsChecked()
                    if self.color == WHITE and KingsChecked[0] == True:
                        # wrong behaviour , can't move
                        squaresToDelete.append(square)
                    if self.color == BLACK and KingsChecked[1] == True:
                        # wrong behaviour , can't move
                        squaresToDelete.append(square)

                    break

        ''' castle situation with check '''

        squaresToDeleteSet = set(squaresToDelete)

        for square in squaresToDeleteSet:
            legalSquareList.remove(square)

        return legalSquareList

    def pseudoLegalMovesSquares(self):
        legalSquareList = []
        self.position = self.getBoardPosition()
        if self.type == PAWN:
            # print(self.position)
            if self.hasMoved == False:
                if self.color == BLACK:
                    if self.chessGame.squares.squareList[self.square.number + NCOLS - 1].piece == None:
                        legalSquareList.append(self.chessGame.squares.squareList[self.square.number + NCOLS - 1])
                        if self.chessGame.squares.squareList[self.square.number + 2 * NCOLS - 1].piece == None:
                            legalSquareList.append(
                                self.chessGame.squares.squareList[self.square.number + 2 * NCOLS - 1])
                else:
                    if self.chessGame.squares.squareList[self.square.number - NCOLS - 1].piece == None:
                        legalSquareList.append(self.chessGame.squares.squareList[self.square.number - NCOLS - 1])
                        if self.chessGame.squares.squareList[self.square.number - 2 * NCOLS - 1].piece == None:
                            legalSquareList.append(
                                self.chessGame.squares.squareList[self.square.number - 2 * NCOLS - 1])
            else:
                if self.color == BLACK:
                    if self.square.number + NCOLS - 1 <= 63:
                        if self.chessGame.squares.squareList[self.square.number + NCOLS - 1].piece == None:
                            legalSquareList.append(self.chessGame.squares.squareList[self.square.number + NCOLS - 1])
                else:
                    if self.chessGame.squares.squareList[self.square.number - NCOLS - 1].piece == None:
                        legalSquareList.append(self.chessGame.squares.squareList[self.square.number - NCOLS - 1])

            if self.color == WHITE:
                new_line = self.position[0] - 1
                new_col1 = self.position[1] - 1
                new_col2 = self.position[1] + 1
            if self.color == BLACK:
                new_line = self.position[0] + 1
                new_col1 = self.position[1] - 1
                new_col2 = self.position[1] + 1

            if self.interior((new_line, new_col1)) == True:
                diagSquare1 = self.chessGame.squares.squareList[self.getSquareNumber((new_line, new_col1)) - 1]
                if diagSquare1.piece != None:
                    if diagSquare1.piece.color != self.color:
                        legalSquareList.append(diagSquare1)
            if self.interior((new_line, new_col2)) == True:
                diagSquare2 = self.chessGame.squares.squareList[self.getSquareNumber((new_line, new_col2)) - 1]
                if diagSquare2.piece != None:
                    if diagSquare2.piece.color != self.color:
                        legalSquareList.append(diagSquare2)

            '''
            En passant
            '''

            # checking left and right.
            # if there is a pawn that moved 2 units last move
            # then I can en passant

            same_line = self.position[0]
            if self.color == WHITE:
                new_line = self.position[0] - 1
            else:
                new_line = self.position[0] + 1
            left_col = self.position[1] - 1
            right_col = self.position[1] + 1

            if self.chessGame.movesHistory:
                if self.interior((same_line, left_col)) == True:

                    if self.chessGame.squares.squareList[self.getSquareNumber((same_line, left_col)) - 1].piece != None:
                        left_piece = self.chessGame.squares.squareList[
                            self.getSquareNumber((same_line, left_col)) - 1].piece
                        if left_piece.type == PAWN:
                            last_move = self.chessGame.movesHistory[-1]
                            if last_move[0] == left_piece and abs(
                                    last_move[1].number - last_move[2].number) == NROWS * 2:
                                diagSquare1 = self.chessGame.squares.squareList[
                                    self.getSquareNumber((new_line, left_col)) - 1]
                                legalSquareList.append(diagSquare1)

                if self.interior((same_line, right_col)) == True:

                    if self.chessGame.squares.squareList[
                        self.getSquareNumber((same_line, right_col)) - 1].piece != None:
                        right_piece = self.chessGame.squares.squareList[
                            self.getSquareNumber((same_line, right_col)) - 1].piece
                        if right_piece.type == PAWN:
                            last_move = self.chessGame.movesHistory[-1]
                            if last_move[0] == right_piece and abs(
                                    last_move[1].number - last_move[2].number) == NROWS * 2:
                                diagSquare2 = self.chessGame.squares.squareList[
                                    self.getSquareNumber((new_line, right_col)) - 1]
                                legalSquareList.append(diagSquare2)

        if self.type == KNIGHT:
            # print(self.position)
            for move in KNIGHT_OFFSET:
                new_line = self.position[0] + move[0]
                new_col = self.position[1] + move[1]
                # print(new_line,new_col)
                if self.interior((new_line, new_col)) == True:
                    squareAux = self.chessGame.squares.squareList[self.getSquareNumber((new_line, new_col)) - 1]
                    if squareAux.piece != None:
                        if squareAux.piece.color == self.color:
                            continue
                    legalSquareList.append(squareAux)

        if self.type == KING:
            for move in KING_OFFSET:
                new_line = self.position[0] + move[0]
                new_col = self.position[1] + move[1]
                if self.interior((new_line, new_col)) == True:
                    squareAux = self.chessGame.squares.squareList[self.getSquareNumber((new_line, new_col)) - 1]
                    if squareAux.piece != None:
                        if squareAux.piece.color == self.color:
                            continue
                    legalSquareList.append(squareAux)
            '''
            ! CASTLE !
            '''
            if self.hasMoved == False:
                for piece in self.chessGame.pieces:
                    if piece.type == ROOK and piece.color == self.color and piece.hasMoved == False and piece.onTable == True:
                        # print(abs(self.square.number - piece.square.number))
                        if abs(self.square.number - piece.square.number) == 3:
                            if self.chessGame.squares.squareList[self.square.number].piece == None and \
                                    self.chessGame.squares.squareList[self.square.number + 1].piece == None:
                                legalSquareList.append(self.chessGame.squares.squareList[self.square.number + 1])
                        if abs(self.square.number - piece.square.number) == 4:
                            if self.chessGame.squares.squareList[self.square.number - 2].piece == None and \
                                    self.chessGame.squares.squareList[self.square.number - 3].piece == None and \
                                    self.chessGame.squares.squareList[self.square.number - 4].piece == None:
                                legalSquareList.append(self.chessGame.squares.squareList[self.square.number - 3])

        if self.type == BISHOP:
            for move in BISHOP_OFFSET:
                new_line = self.position[0] + move[0]
                new_col = self.position[1] + move[1]
                while self.interior((new_line, new_col)) == True:
                    squareAux = self.chessGame.squares.squareList[self.getSquareNumber((new_line, new_col)) - 1]
                    if squareAux.piece != None:
                        if squareAux.piece.color != self.color:
                            legalSquareList.append(squareAux)
                        break
                    legalSquareList.append(squareAux)
                    new_line = new_line + move[0]
                    new_col = new_col + move[1]

        if self.type == ROOK:
            for move in ROOK_OFFSET:
                new_line = self.position[0] + move[0]
                new_col = self.position[1] + move[1]
                while self.interior((new_line, new_col)) == True:
                    squareAux = self.chessGame.squares.squareList[self.getSquareNumber((new_line, new_col)) - 1]
                    if squareAux.piece != None:
                        if squareAux.piece.color != self.color:
                            legalSquareList.append(squareAux)
                        break
                    legalSquareList.append(squareAux)
                    new_line = new_line + move[0]
                    new_col = new_col + move[1]

        if self.type == QUEEN:
            for move in KING_OFFSET:
                new_line = self.position[0] + move[0]
                new_col = self.position[1] + move[1]
                while self.interior((new_line, new_col)) == True:
                    squareAux = self.chessGame.squares.squareList[self.getSquareNumber((new_line, new_col)) - 1]
                    if squareAux.piece != None:
                        if squareAux.piece.color != self.color:
                            legalSquareList.append(squareAux)
                        break
                    legalSquareList.append(squareAux)
                    new_line = new_line + move[0]
                    new_col = new_col + move[1]

        return legalSquareList

    def moveToSquare(self, square):
        if square != None:
            self.hasMoved = True
            if square.piece != None:
                square.piece.onTable = False
                square.piece = None
            self.square.piece = None
            self.square = square
            square.piece = self
            self.position = self.getBoardPosition()
            self.setCorrectPosition()
            if self.type == PAWN and self.color == WHITE:
                if 1 <= square.number and square.number <= 8:
                    self.type = QUEEN
                    self.setImage()
                    self.setPoints()
            if self.type == PAWN and self.color == BLACK:
                if 57 <= square.number and square.number <= 64:
                    self.type = QUEEN
                    self.setImage()
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
            self.points = 11
            # -> I don't think he has any evaluation of points

    def takeFromTable(self):
        self.onTable = False
        self.square.piece = None
        self.square = None

    def getSquareNumber(self, position):
        return (position[0] * NCOLS + position[1] + 1)

    def getBoardPosition(self):
        line = (self.square.number - 1) // NCOLS
        column = (self.square.number - 1) % NROWS
        return (line, column)

    def setImage(self):
        self.image = pygame.image.load("assets/white_pawn.png").convert()

        if self.type == PAWN:
            if self.color == WHITE:
                self.image = pygame.image.load("assets/white_pawn.png").convert()
            else:
                self.image = pygame.image.load("assets/black_pawn.png").convert()

        if self.type == ROOK:
            if self.color == WHITE:
                self.image = pygame.image.load("assets/white_rook.png").convert()
            else:
                self.image = pygame.image.load("assets/black_rook.png").convert()

        if self.type == BISHOP:
            if self.color == WHITE:
                self.image = pygame.image.load("assets/white_bishop.png").convert()
            else:
                self.image = pygame.image.load("assets/black_bishop.png").convert()

        if self.type == KNIGHT:
            if self.color == WHITE:
                self.image = pygame.image.load("assets/white_knight.png").convert()
            else:
                self.image = pygame.image.load("assets/black_knight.png").convert()

        if self.type == QUEEN:
            if self.color == WHITE:
                self.image = pygame.image.load("assets/white_queen.png").convert()
            else:
                self.image = pygame.image.load("assets/black_queen.png").convert()

        if self.type == KING:
            if self.color == WHITE:
                self.image = pygame.image.load("assets/white_king.png").convert()
            else:
                self.image = pygame.image.load("assets/black_king.png").convert()

        self.image.set_colorkey((100, 100, 100))

    def render(self, surf):

        if self.onTable == False:
            return

        surf.blit(self.image, self.imagePosition)
        # pygame.draw.circle(surf, self.color, (self.square.getScreenPosition()[0] + TILEWIDTH / 2 , self.square.getScreenPosition()[1] + TILEHEIGHT / 2), TILEHEIGHT / 2)
