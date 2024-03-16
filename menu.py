import pygame
from constants import *


class GameMenu:
    def __init__(self):
        self.surf = pygame.Surface(SCREENSIZE)
        self.font = pygame.font.Font(None, 100)
        self.welcomeMessage = self.font.render("Welcome to Pixel Chess!", True, WHITE)
        self.welcomeMessagePos = (100, 60)
        self.buttonDimensions = (300, 200)
        self.casualRectangle = pygame.Rect(106, 700, self.buttonDimensions[0], self.buttonDimensions[1])
        self.botRectangle = pygame.Rect(106 + 512, 700, self.buttonDimensions[0], self.buttonDimensions[1])
        self.casualMessage = self.font.render("Casual", True, BLACK)
        self.casualMessagePos = (133, 765)
        self.botMessage = self.font.render("Bot", True, BLACK)
        self.botMessagePos = (190 + 512, 765)
        self.menuImage = pygame.image.load("assets/IntroImage.png").convert()

    def handleEvents(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = event.pos
                if self.casualRectangle.collidepoint(mouse_pos):
                    return PLAYING_CASUAL
                if self.botRectangle.collidepoint(mouse_pos):
                    return PLAYING_BOT
        return MENU

    def render(self):
        self.surf.fill((50, 50, 50))
        self.surf.blit(self.welcomeMessage, self.welcomeMessagePos)
        self.surf.blit(self.menuImage, (0, 0))
        pygame.draw.rect(self.surf, BLACK, self.casualRectangle, 8)
        pygame.draw.rect(self.surf, BLACK, self.botRectangle, 8)
        self.surf.blit(self.casualMessage, self.casualMessagePos)
        self.surf.blit(self.botMessage, self.botMessagePos)
