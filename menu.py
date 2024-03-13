import pygame
from constants import *


class GameMenu:
    def __init__(self):
        self.surf = pygame.Surface(SCREENSIZE)
        self.font = pygame.font.Font(None, 100)
        self.welcomeMessage = self.font.render("Welcome to Pixel Chess!", True, WHITE)
        self.welcomeMessagePos = (100, 60)
        self.buttonDimensions = (300, 200)
        self.casualRectangle = pygame.Rect(106, 400, self.buttonDimensions[0], self.buttonDimensions[1])
        self.botRectangle = pygame.Rect(106 + 512, 400, self.buttonDimensions[0], self.buttonDimensions[1])
        self.casualMessage = self.font.render("Casual", True, (50, 50, 50))
        self.casualMessagePos = (133, 465)
        self.botMessage = self.font.render("Bot", True, (50, 50, 50))
        self.botMessagePos = (190 + 512, 465)

    def handleEvents(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = event.pos
                if self.casualRectangle.collidepoint(mouse_pos):
                    return PLAYING_CASUAL
                if self.casualRectangle.collidepoint(mouse_pos):
                    return PLAYING_BOT
        return MENU

    def render(self):
        self.surf.fill((50, 50, 50))
        self.surf.blit(self.welcomeMessage, self.welcomeMessagePos)
        pygame.draw.rect(self.surf, WHITE, self.casualRectangle)
        pygame.draw.rect(self.surf, WHITE, self.botRectangle)
        self.surf.blit(self.casualMessage, self.casualMessagePos)
        self.surf.blit(self.botMessage, self.botMessagePos)
