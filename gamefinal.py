import pygame
from constants import *


class GameFinal:
    def __init__(self):
        self.surf = pygame.Surface(SCREENSIZE)
        self.font = pygame.font.Font(None, 100)
        self.winner = None
        # self.winnerMessage = self.font.render("Winner is {}".format(self.winner), True, WHITE)
        self.winnerMessagePos = (170, 200)

    def handleEvents(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                return MENU
        return FINAL_STATEMENT

    def updateWinnerMessage(self, winner):
        if winner == WHITE:
            self.winnerMessage = self.font.render("Winner is WHITE", True, WHITE)
        if winner == BLACK:
            self.winnerMessage = self.font.render("Winner is BLACK", True, WHITE)

    def setWinner(self, winner):
        self.winner = winner
        self.updateWinnerMessage(winner)

    def render(self):
        self.surf.fill((50, 50, 50))
        self.surf.blit(self.winnerMessage, self.winnerMessagePos)
