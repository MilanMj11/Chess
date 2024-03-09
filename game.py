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
        self.holdingClick = False
        self.mouse_pos = None
        # self.chessGame = Chess()

    def startGame(self):
        self.chessGame = Chess()

    def update(self):

        self.clock.tick(60)  # 60 FPS , doesn't really matter right now
        self.checkGameEvents()
        self.render()

    def checkGameEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.mouse_pos = event.pos
                    self.holdingClick = True
                    self.chessGame.handleClick(self.mouse_pos, LEFT_CLICK_PRESS)
                if event.button == 3:
                    self.mouse_pos = event.pos
                    self.chessGame.unselectEverything()
                    self.holdingClick = False
                    self.chessGame.handleClick(self.mouse_pos, RIGHT_CLICK)
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.mouse_pos = event.pos
                    self.holdingClick = False
                    self.chessGame.handleClick(self.mouse_pos, LEFT_CLICK_RELEASE)

        # print(self.holdingClick)
        self.chessGame.holdingClick(self.mouse_pos, self.holdingClick)
    def render(self):
        self.chessGame.render(self.screen)
        pygame.display.update()
