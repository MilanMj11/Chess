import pygame
from constants import *
from squares import Squares
from chess import Chess
from menu import GameMenu
from gamefinal import GameFinal
from AI import AI

class GameController:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Chess")
        self.display = pygame.display.set_mode(SCREENSIZE)
        self.chessScreen = pygame.Surface(SCREENSIZE)
        self.botChessGame = None
        self.menuScreen = GameMenu()
        self.finalScreen = GameFinal()
        # self.gameScreen = pygame.display.set_mode(GAMESCREENSIZE)
        self.clock = pygame.time.Clock()
        self.holdingClick = False
        self.mouse_pos = None
        self.gameState = MENU

    def startGame(self):
        pass
        # self.casualChessGame = Chess()

    def update(self):

        if self.gameState == PLAYING_BOT and self.botChessGame != None:
            self.AI.makeMove(self.AI.findBestMove())

        self.clock.tick(90)  # 60 FPS , doesn't really matter right now
        self.checkGameEvents()
        self.render()

    def checkGameEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if self.gameState == PLAYING_CASUAL:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.gameState = MENU

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.mouse_pos = event.pos
                        self.holdingClick = True
                        self.casualChessGame.handleClick(self.mouse_pos, LEFT_CLICK_PRESS)
                    if event.button == 3:
                        self.mouse_pos = event.pos
                        self.casualChessGame.unselectEverything()
                        self.holdingClick = False
                        self.casualChessGame.handleClick(self.mouse_pos, RIGHT_CLICK)
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.mouse_pos = event.pos
                        self.holdingClick = False
                        self.casualChessGame.handleClick(self.mouse_pos, LEFT_CLICK_RELEASE)

            if self.gameState == PLAYING_BOT:
                if self.botChessGame.turn != self.AI.color:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.gameState = MENU

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            self.mouse_pos = event.pos
                            self.holdingClick = True
                            self.botChessGame.handleClick(self.mouse_pos, LEFT_CLICK_PRESS)
                        if event.button == 3:
                            self.mouse_pos = event.pos
                            self.botChessGame.unselectEverything()
                            self.holdingClick = False
                            self.botChessGame.handleClick(self.mouse_pos, RIGHT_CLICK)
                    if event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1:
                            self.mouse_pos = event.pos
                            self.holdingClick = False
                            self.botChessGame.handleClick(self.mouse_pos, LEFT_CLICK_RELEASE)

            if self.gameState == MENU:
                self.gameState = self.menuScreen.handleEvents(event)
                if self.gameState == PLAYING_CASUAL:
                    self.casualChessGame = Chess()
                if self.gameState == PLAYING_BOT:
                    self.botChessGame = Chess()
                    self.AI = AI(self.botChessGame, BLACK)

            if self.gameState == FINAL_STATEMENT:
                self.gameState = self.finalScreen.handleEvents(event)

        # print(self.holdingClick)
        if self.gameState == PLAYING_BOT:
            self.botChessGame.holdingClick(self.mouse_pos, self.holdingClick)
        if self.gameState == PLAYING_CASUAL:
            self.casualChessGame.holdingClick(self.mouse_pos, self.holdingClick)

    def render(self):

        if self.gameState == PLAYING_CASUAL:
            self.casualChessGame.render(self.chessScreen)
            self.display.blit(self.chessScreen, (0, 0))
            gameWinner = self.casualChessGame.gameOver
            if gameWinner != None:
                self.gameState = FINAL_STATEMENT
                self.finalScreen.setWinner(gameWinner)

        if self.gameState == PLAYING_BOT:
            self.botChessGame.render(self.chessScreen)
            self.display.blit(self.chessScreen, (0, 0))
            gameWinner = self.botChessGame.gameOver
            if gameWinner != None:
                self.gameState = FINAL_STATEMENT
                self.finalScreen.setWinner(gameWinner)

        if self.gameState == MENU:
            self.menuScreen.render()
            self.display.blit(self.menuScreen.surf, (0, 0))

        if self.gameState == FINAL_STATEMENT:
            self.finalScreen.render()
            self.display.blit(self.finalScreen.surf, (0, 0))

        pygame.display.update()
