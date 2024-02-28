# Inside MainMenu.py
import pygame
import sys
from .BaseMenu import BaseMenu
from .InstructionsMenu import InstructionsMenu



class MainMenu(BaseMenu):
    def __init__(self, screen, screen_width, screen_height):
        super().__init__(screen, screen_width, screen_height, './imgs/menuBackground.png')

    def run(self):
        while True:
            self.screen.blit(self.background_image, (0, 0))
            mx, my = pygame.mouse.get_pos()

            button_1 = pygame.Rect(70, 500, 250, 50)  # posx, posy, largura, altura
            button_2 = pygame.Rect(70, 560, 250, 50)
            button_3 = pygame.Rect(70, 620, 250, 50)

            if button_1.collidepoint((mx, my)):
                if self.click:
                    self.start_game()
            if button_2.collidepoint((mx, my)):
                if self.click:
                    instructions_menu = InstructionsMenu(self.screen, self.screen_width, self.screen_height)
                    instructions_menu.run()
            if button_3.collidepoint((mx, my)):
                if self.click:
                    pygame.quit()
                    sys.exit()

            pygame.draw.rect(self.screen, self.yellow, button_1)
            pygame.draw.rect(self.screen, self.yellow, button_2)
            pygame.draw.rect(self.screen, self.yellow, button_3)

            self.draw_text('Start Game', self.backColor, 90, 510)
            self.draw_text('Instructions', self.backColor, 90, 570)
            self.draw_text('Exit', self.backColor, 90, 630)

            self.handle_events()
            self.update_display()

    def start_game(self):
        print("Start game placeholder")
