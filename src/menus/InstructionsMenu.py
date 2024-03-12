# Inside MainMenu.py
import pygame
from .BaseMenu import BaseMenu


class InstructionsMenu(BaseMenu):
    def __init__(self, screen, screen_width, screen_height):
        super().__init__(screen, screen_width, screen_height, './imgs/instructions.png')

    def run(self):
        running = True
        while running:
            self.screen.blit(self.background_image, (0, 0))
            mx, my = pygame.mouse.get_pos()

            button_1 = pygame.Rect(70, 760, 250, 50) #posx, posy, largura, altura

            if button_1.collidepoint((mx, my)):
                if self.click:
                    running = False

            pygame.draw.rect(self.screen, self.orange, button_1)
            self.draw_text('Back', self.backColor, 90, 770)

            self.handle_events()
            self.update_display()

    def back_mainMenu(self):
        print("Back to MainMenu")
