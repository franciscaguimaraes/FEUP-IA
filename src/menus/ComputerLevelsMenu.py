import pygame
from .BaseMenu import BaseMenu
from src import GameController

""" Initializes the computer levels menu with UI elements for selecting difficulty levels.
        @param screen: The main game screen or surface where the menu will be drawn.
        @param screen_width: The width of the screen in pixels.
        @param screen_height: The height of the screen in pixels.
        @param mode: The game mode that determines the type of match (Player vs Computer, Computer vs Computer).
    """
class ComputerLevelsMenu(BaseMenu):
    def __init__(self, screen, screen_width, screen_height, mode, board_size):
        super().__init__(screen, screen_width, screen_height, './imgs/computerLevels.png')
        self.mode = mode
        self.levelB = 0
        self.levelR = 0
        self.board_size = board_size

    """ Runs the computer levels menu, handling user input to select difficulty levels and start the game.
        """
    def run(self):
        running = True
        while running:
            self.screen.blit(self.background_image, (0, 0))
            mx, my = pygame.mouse.get_pos()

            button_1 = pygame.Rect(230, 370, 280, 70)  # posx, posy, largura, altura
            button_2 = pygame.Rect(230, 480, 280, 70)
            button_3 = pygame.Rect(230, 600, 280, 70)

            button_4 = pygame.Rect(725, 370, 280, 70)
            button_5 = pygame.Rect(725, 480, 280, 70)
            button_6 = pygame.Rect(725, 600, 280, 70)

            button_7 = pygame.Rect(70, 760, 250, 50)

            # buttons for computer BLUE levels
            if button_1.collidepoint((mx, my)):  # level 1
                if self.click:
                    self.levelB = 1
                    print(self.levelB)
            if button_2.collidepoint((mx, my)):  # level 2
                if self.click:
                    self.levelB = 2
                    print(self.levelB)

            if button_3.collidepoint((mx, my)):  # level 3
                if self.click:
                    self.levelB = 3
                    print(self.levelB)


            # buttons for computer RED levels
            if button_4.collidepoint((mx, my)):  # level 1
                if self.click:
                    self.levelR = 1
                    print(self.levelR)
            if button_5.collidepoint((mx, my)):  # level 2
                if self.click:
                    self.levelR = 2
                    print(self.levelR)

            if button_6.collidepoint((mx, my)):  # level 3
                if self.click:
                    self.levelR = 3
                    print(self.levelR)


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

    """ Starts the game with the selected difficulty levels for the computer players.
            @param mode: The game mode to be used.
            @param difficulty1: The difficulty level for the first computer player.
            @param difficulty2: The difficulty level for the second computer player.
        """
    def start_game(self, mode, difficulty1, difficulty2):
        game = GameController.GameController(600, 600, self.board_size, mode, difficulty1, difficulty2)
        game.run()