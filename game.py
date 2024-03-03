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
        # self.chessGame = Chess()

    def startGame(self):
        self.chessGame = Chess()

    def update(self):

        self.clock.tick(60) # 60 FPS , doesn't really matter right now
        self.checkGameEvents()
        self.render()

    def checkGameEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = event.pos
                    self.chessGame.handleClick(mouse_pos)


    def render(self):
        self.chessGame.render(self.screen)
        pygame.display.update()