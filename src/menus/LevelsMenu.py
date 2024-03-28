import pygame
from .BaseMenu import BaseMenu
from src import GameController


class LevelsMenu(BaseMenu):
    def __init__(self, screen, screen_width, screen_height, mode, turn):
        super().__init__(screen, screen_width, screen_height, './imgs/gameLevels.png')
        self.mode = mode
        self.turn = turn

    def run(self):
        running = True
        while running:
            self.screen.blit(self.background_image, (0, 0))
            mx, my = pygame.mouse.get_pos()

            button_1 = pygame.Rect(450, 280, 350, 80)  # posx, posy, largura, altura
            button_2 = pygame.Rect(450, 430, 350, 80)
            button_3 = pygame.Rect(450, 580, 350, 80)
            button_4 = pygame.Rect(70, 760, 250, 50)

            if button_1.collidepoint((mx, my)):  # level 1
                if self.click:
                    self.start_game(self.mode, 1, self.turn)
            if button_2.collidepoint((mx, my)):  # level 2
                if self.click:
                    if self.click:
                        self.start_game(self.mode, 2, self.turn)
            if button_3.collidepoint((mx, my)):  # level 3
                if self.click:
                    self.start_game(self.mode, 3, self.turn)
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
