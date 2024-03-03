import pygame
from constants import *
from squares import Squares
from chess import Chess

class GameController:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Chess")
        self.screen = pygame.display.set_mode(SCREENSIZE)
        self.clock = pygame.time.Clock()
        self.chessGame = Chess()

    def startGame(self):
        pass

    def update(self):

        self.clock.tick(60) # 60 FPS , doesn't really matter right now
        self.checkEvents()
        self.render()

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

    def render(self):
        self.chessGame.render(self.screen)
        pygame.display.update()