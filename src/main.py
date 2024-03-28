import pygame
from menus.MainMenu import MainMenu

def main():
    pygame.init()

    screen_width, screen_height = 1250, 850
    screen = pygame.display.set_mode((screen_width, screen_height))

    main_menu = MainMenu(screen, screen_width, screen_height)
    main_menu.run()

if __name__ == "__main__":
    main()