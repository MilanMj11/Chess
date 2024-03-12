import pygame
from constants import *
from squares import Squares
from chess import Chess
from menu import GameMenu

class GameController:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Chess")
        self.display = pygame.display.set_mode(SCREENSIZE)
        self.chessScreen = pygame.Surface(SCREENSIZE)
        self.menuScreen = pygame.Surface(SCREENSIZE)
        # self.gameScreen = pygame.display.set_mode(GAMESCREENSIZE)
        self.clock = pygame.time.Clock()
        self.holdingClick = False
        self.mouse_pos = None
        self.gameState = MENU

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

            if self.gameState == PLAYING_CASUAL:
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

            if self.gameState == MENU:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.gameState = PLAYING_CASUAL

        # print(self.holdingClick)
        if self.gameState == PLAYING_CASUAL:
            self.chessGame.holdingClick(self.mouse_pos, self.holdingClick)

    def render(self):

        if self.gameState == PLAYING_CASUAL:
            self.chessGame.render(self.chessScreen)
            self.display.blit(self.chessScreen, (0,0))

        if self.gameState == MENU:
            self.menuScreen.fill((50, 50, 50))
            self.display.blit(self.menuScreen, (0,0))

        pygame.display.update()
