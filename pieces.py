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
        # self.Squares = Squares()

    def interior(self, position):
        if position[0] >= 0 and position[0] < NCOLS and position[1] >= 0 and position[1] < NROWS:
            return True
        return False

    def legalMovesSquares(self):
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

    def getSquareNumber(self, position):
        return (position[0] * NCOLS + position[1] + 1)

    def getBoardPosition(self):
        line = (self.square.number - 1) // NCOLS
        column = (self.square.number - 1) % NROWS
        return (line, column)

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
