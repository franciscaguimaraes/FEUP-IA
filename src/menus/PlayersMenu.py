import pygame
from .BaseMenu import BaseMenu
from src.Board import Board


class PlayersMenu(BaseMenu):
    def __init__(self, screen, screen_width, screen_height):
        super().__init__(screen, screen_width, screen_height, './imgs/playersMenu.png')

    def run(self):
        running = True
        while running:
            self.screen.blit(self.background_image, (0, 0))
            mx, my = pygame.mouse.get_pos()

            button_1 = pygame.Rect(490, 265, 350, 50)  # posx, posy, largura, altura
            button_2 = pygame.Rect(490, 385, 350, 50)
            button_3 = pygame.Rect(490, 505, 350, 50)
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

            pygame.draw.rect(self.screen, self.backColor, button_1)
            pygame.draw.rect(self.screen, self.backColor, button_2)
            pygame.draw.rect(self.screen, self.backColor, button_3)
            pygame.draw.rect(self.screen, self.orange, button_4)

            self.draw_text('Player vs Player', self.orange, 500, 280)
            self.draw_text('Player vs Computer', self.orange, 500, 400)
            self.draw_text('Computer vs Computer', self.orange, 500, 520)
            self.draw_text('Back', self.backColor, 90, 770)

            self.handle_events()
            self.update_display()

    def start_game(self):
        game = Board(600, 600)
        game.run()
        print("Start game placeholder")
