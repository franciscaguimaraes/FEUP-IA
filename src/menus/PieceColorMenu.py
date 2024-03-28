import pygame
from .BaseMenu import BaseMenu
from src import GameController

class PieceColorMenu(BaseMenu):
    def __init__(self, screen, screen_width, screen_height):
        super().__init__(screen, screen_width, screen_height, './imgs/selectColorMenu.png')

    def run(self):
        running = True
        while running:
            self.screen.blit(self.background_image, (0, 0))
            mx, my = pygame.mouse.get_pos()

            button_1 = pygame.Rect(450, 330, 350, 80)  # posx, posy, largura, altura
            button_2 = pygame.Rect(450, 480, 350, 80)
            button_4 = pygame.Rect(70, 760, 250, 50)

            if button_1.collidepoint((mx, my)):  # Start first
                if self.click:
                    self.start_game(1, None, 'B')
            if button_2.collidepoint((mx, my)):  # Start second
                if self.click:
                    if self.click:
                        self.start_game(1, None, 'R')
            if button_4.collidepoint((mx, my)):
                if self.click:
                    running = False

            pygame.draw.rect(self.screen, self.orange, button_4)
            self.draw_text('Back', self.backColor, 90, 770)

            self.handle_events()
            self.update_display()

    def start_game(self, mode, difficulty, turn):
        game = GameController.GameController(600, 600, 8, mode, difficulty, None, turn)
        game.run()
