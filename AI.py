import copy

import pygame
from constants import *

class AI:
    def __init__(self, chessGame, color):
        self.chessGame = chessGame # to know what game I'm playing
        self.color = color # to know what color the AI is playing with ( WHITE / BLACK )

    def findBestMove(self, depth):
        # Precaution in case I call it on the wrong turn
        if self.chessGame.turn == WHITE_TURN and self.color == BLACK:
            return None
        if self.chessGame.turn == BLACK_TURN and self.color == WHITE:
            return None

        minScore = 100000
        bestMove = None

        for piece in self.chessGame.pieces:
            if piece.onTable == True and piece.color == self.color:
                # chessGameCopy = copy.copy(self.chessGame)
                for square in piece.actualLegalMovesSquares():
                    simulateInfo = piece.simulateMove(square)
                    self.chessGame.checkIfGameOver()

                    positionScore = self.minimax(depth - 1, float('-inf'), float('inf'), True)

                    # positionEvaluation = self.chessGame.positionEvaluation()
                    piece.undoSimulatedMove(simulateInfo[0], simulateInfo[1], simulateInfo[2], simulateInfo[3])
                    self.chessGame.gameOver = None

                    # positionScore = self.chessGame.interpretEvaluation(positionEvaluation)

                    '''
                    if self.color == BLACK:
                        positionScore *= -1
                    '''

                    if positionScore < minScore:
                        minScore = positionScore
                        bestMove = (piece, square)

        # bestMove = (piece, toSquare)
        return bestMove

    def minimax(self, depth, alpha, beta, maximizingPlayer):
        # self.chessGame.checkIfGameOver()
        if depth == 0 or self.chessGame.gameOver == True:
            return self.chessGame.interpretEvaluation(self.chessGame.positionEvaluation())

        if maximizingPlayer:
            maxScore = float('-inf')
            for piece in self.chessGame.pieces:
                if piece.onTable and piece.color != self.color:
                    for square in piece.actualLegalMovesSquares():
                        simulateInfo = piece.simulateMove(square)
                        self.chessGame.checkIfGameOver()

                        score = self.minimax(depth - 1, alpha, beta, False)
                        piece.undoSimulatedMove(simulateInfo[0], simulateInfo[1], simulateInfo[2], simulateInfo[3])
                        self.chessGame.gameOver = None

                        maxScore = max(maxScore, score)
                        '''
                        alpha = max(alpha, score)
                        if beta <= alpha:
                            break  # Beta cut-off
                        '''

            return maxScore
        else:
            minScore = float('inf')
            for piece in self.chessGame.pieces:
                if piece.onTable and piece.color == self.color:
                    for square in piece.actualLegalMovesSquares():
                        simulateInfo = piece.simulateMove(square)
                        self.chessGame.checkIfGameOver()

                        score = self.minimax(depth - 1, alpha, beta, True)
                        piece.undoSimulatedMove(simulateInfo[0], simulateInfo[1], simulateInfo[2], simulateInfo[3])
                        self.chessGame.gameOver = None

                        minScore = min(minScore, score)
                        '''
                        beta = min(beta, score)
                        if beta <= alpha:
                            break  # Alpha cut-off
                        '''

            return minScore

    def makeMove(self, move):
        if self.chessGame.turn == WHITE_TURN and self.color == BLACK:
            return
        if self.chessGame.turn == BLACK_TURN and self.color == WHITE:
            return

        piece = move[0]
        square = move[1]

        castled = False

        if piece.type == KING:
            # print("OK")
            if abs(square.number - piece.square.number) == 2:
                # print("BETTER")
                if square.number > piece.square.number:
                    rook = self.chessGame.squares.squareList[square.number].piece
                    rook.moveToSquare(self.chessGame.squares.squareList[square.number - 2])
                    self.chessGame.movesHistory.append("Small Castle")
                    castled = True

                if square.number < piece.square.number:
                    rook = self.chessGame.squares.squareList[square.number - 3].piece
                    rook.moveToSquare(self.chessGame.squares.squareList[square.number])
                    self.chessGame.movesHistory.append("Big Castle")
                    castled = True

        if castled == False:
            self.chessGame.movesHistory.append((piece, piece.square, square))


        piece.moveToSquare(square)
        self.chessGame.checkIfGameOver()
        if self.color == BLACK:
            self.chessGame.turn = WHITE_TURN
        else:
            self.chessGame.turn = BLACK_TURN
