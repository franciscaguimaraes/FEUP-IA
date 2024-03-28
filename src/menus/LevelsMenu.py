import pygame
from .BaseMenu import BaseMenu
from src import GameController


class LevelsMenu(BaseMenu):

    """ Initializes the levels menu with game settings and background.
        @param screen: The main game screen or surface where the menu will be drawn.
        @param screen_width: The width of the screen in pixels.
        @param screen_height: The height of the screen in pixels.
        @param mode: The game mode, determining how the game logic and interactions are handled.
        @param turn: Indicates who starts the game, the player or the computer.
    """
    def __init__(self, screen, screen_width, screen_height, mode, turn):
        super().__init__(screen, screen_width, screen_height, './imgs/gameLevels.png')
        self.mode = mode
        self.turn = turn

    """ Runs the levels menu, allowing the user to select a difficulty level for the game.
        Handles user input to select levels and start the game or go back to the previous menu.
    """
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

    """ Starts a new game with the selected difficulty level.
        @param mode: The game mode, determining how the game logic and interactions are handled.
        @param difficulty: The difficulty level selected for the computer opponent.
        @param turn: Indicates who starts the game, the player or the computer.
    """
    def start_game(self, mode, difficulty, turn):
        game = GameController.GameController(600, 600, 8, mode, difficulty, None, turn)
        game.run()
