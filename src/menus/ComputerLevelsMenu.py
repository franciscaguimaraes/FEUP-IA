import pygame
from .BaseMenu import BaseMenu
from src import GameController


class ComputerLevelsMenu(BaseMenu):

    """ Initializes the computer levels menu with UI elements for selecting difficulty levels.
        @param screen: The main game screen or surface where the menu will be drawn.
        @param screen_width: The width of the screen in pixels.
        @param screen_height: The height of the screen in pixels.
        @param mode: The game mode that determines the type of match (Player vs Computer, Computer vs Computer).
    """
    def __init__(self, screen, screen_width, screen_height, mode):
        super().__init__(screen, screen_width, screen_height, './imgs/computerLevels.png')
        self.mode = mode
        self.levelB = 0
        self.levelR = 0

    """ Runs the computer levels menu, handling user input to select difficulty levels and start the game.
    """
    def run(self):
        running = True
        while running:
            self.screen.blit(self.background_image, (0, 0))
            mx, my = pygame.mouse.get_pos()

            button_1 = pygame.Rect(450, 280, 350, 80)  # posx, posy, largura, altura
            button_2 = pygame.Rect(450, 430, 350, 80)
            button_3 = pygame.Rect(450, 580, 350, 80)

            button_4 = pygame.Rect(450, 280, 350, 80)
            button_5 = pygame.Rect(450, 430, 350, 80)
            button_6 = pygame.Rect(450, 580, 350, 80)

            button_7 = pygame.Rect(70, 760, 250, 50)

            # buttons for computer BLUE levels
            if button_1.collidepoint((mx, my)):  # level 1
                if self.click:
                    self.levelB = 1
            if button_2.collidepoint((mx, my)):  # level 2
                if self.click:
                    self.levelB = 2
            if button_3.collidepoint((mx, my)):  # level 3
                if self.click:
                    self.levelB = 3

            # buttons for computer RED levels
            if button_4.collidepoint((mx, my)):  # level 1
                if self.click:
                    self.levelR = 1
            if button_5.collidepoint((mx, my)):  # level 2
                if self.click:
                    self.levelR = 2
            if button_6.collidepoint((mx, my)):  # level 3
                if self.click:
                    self.levelR = 3

            # Back button
            if button_7.collidepoint((mx, my)):
                if self.click:
                    running = False

            if self.levelB != 0 and self.levelR != 0:
                self.start_game(self.mode, self.levelB, self.levelR)

            pygame.draw.rect(self.screen, self.orange, button_7)
            self.draw_text('Back', self.backColor, 90, 770)
            self.handle_events()
            self.update_display()

    # def __init__(self, width, height, board_size=8, mode=None, difficulty1=None, difficulty2=None, turn='B'):
    """ Starts the game with the selected difficulty levels for the computer players.
        @param mode: The game mode to be used.
        @param difficulty1: The difficulty level for the first computer player.
        @param difficulty2: The difficulty level for the second computer player.
    """
    def start_game(self, mode, difficulty1, difficulty2):
        game = GameController.GameController(600, 600, 8, mode, difficulty1, difficulty2)
        game.run()
