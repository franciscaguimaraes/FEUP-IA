import pygame
from .BaseMenu import BaseMenu
from .PlayersMenu import PlayersMenu


class BoardSizeMenu(BaseMenu):
    """ Initializes the board size menu with a background image and settings.
            @param screen: The main game screen or surface where the menu will be drawn.
            @param screen_width: The width of the screen in pixels.
            @param screen_height: The height of the screen in pixels.
        """
    def __init__(self, screen, screen_width, screen_height):
        super().__init__(screen, screen_width, screen_height, './imgs/boardSize.png')

    """ Runs the board size menu, displaying the menu options and handling user interactions. """
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
                    players_menu = PlayersMenu(self.screen, self.screen_width, self.screen_height, 8)
                    players_menu.run()
            if button_2.collidepoint((mx, my)):  # Start second
                if self.click:
                    players_menu = PlayersMenu(self.screen, self.screen_width, self.screen_height, 6)
                    players_menu.run()
            if button_4.collidepoint((mx, my)):
                if self.click:
                    running = False

            pygame.draw.rect(self.screen, self.orange, button_4)
            self.draw_text('Back', self.backColor, 90, 770)

            self.handle_events()
            self.update_display()