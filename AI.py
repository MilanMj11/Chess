import copy

import pygame
from constants import *

class AI:
    def __init__(self, chessGame, color):
        self.chessGame = chessGame # to know what game I'm playing
        self.color = color # to know what color the AI is playing with ( WHITE / BLACK )

    def findBestMove(self):
        # Precaution in case I call it on the wrong turn
        if self.chessGame.turn == WHITE_TURN and self.color == BLACK:
            return None
        if self.chessGame.turn == BLACK_TURN and self.color == WHITE:
            return None

        maxScore = -10000
        bestMove = None

        for piece in self.chessGame.pieces:
            if piece.onTable == True and piece.color == self.color:
                # chessGameCopy = copy.copy(self.chessGame)
                for square in piece.actualLegalMovesSquares():
                    simulateInfo = piece.simulateMove(square)
                    positionEvaluation = self.chessGame.positionEvaluation()
                    piece.undoSimulatedMove(simulateInfo[0], simulateInfo[1])

                    positionScore = self.chessGame.interpretEvaluation(positionEvaluation)
                    if self.color == BLACK:
                        positionScore *= -1

                    if positionScore > maxScore:
                        maxScore = positionScore
                        bestMove = (piece, square)

        # bestMove = (piece, toSquare)
        return bestMove

    def makeMove(self, move):
        if self.chessGame.turn == WHITE_TURN and self.color == BLACK:
            return
        if self.chessGame.turn == BLACK_TURN and self.color == WHITE:
            return

        piece = move[0]
        square = move[1]

        piece.moveToSquare(square)
        self.chessGame.checkIfGameOver()
        if self.color == BLACK:
            self.chessGame.turn = WHITE_TURN
        else:
            self.chessGame.turn = BLACK_TURN
