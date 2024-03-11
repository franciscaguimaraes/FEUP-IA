import pygame
import sys
from .BaseMenu import BaseMenu


class PlayersMenu(BaseMenu):
    def __init__(self, screen, screen_width, screen_height):
        super().__init__(screen, screen_width, screen_height, './imgs/playersMenu.png')

    def run(self):
        running = True
        while running:
            self.screen.blit(self.background_image, (0, 0))
            mx, my = pygame.mouse.get_pos()

            button_1 = pygame.Rect(100, 500, 350, 50)  #posx, posy, largura, altura
            button_2 = pygame.Rect(100, 600, 350, 50)
            button_3 = pygame.Rect(100, 700, 350, 50)
            button_4 = pygame.Rect(70, 760, 350, 50)

            if button_1.collidepoint((mx, my)):
                if self.click:
                    self.start_game()
            if button_2.collidepoint((mx, my)):
                if self.click:
                    self.start_game()
            if button_3.collidepoint((mx, my)):
                if self.click:
                    self.start_game()
            if button_4.collidepoint((mx, my)):
                if self.click:
                    running = False

            pygame.draw.rect(self.screen, self.black, button_1)
            pygame.draw.rect(self.screen, self.black, button_2)
            pygame.draw.rect(self.screen, self.black, button_3)
            pygame.draw.rect(self.screen, self.orange, button_4)


            self.draw_text('Player vs Player', self.backColor, 90, 510)
            self.draw_text('Player vs Computer', self.backColor, 90, 570)
            self.draw_text('Computer vs Computer', self.backColor, 90, 630)
            self.draw_text('Back', self.backColor, 90, 770)

            self.handle_events()
            self.update_display()

    def start_game(self):
        print("Start game placeholder")
