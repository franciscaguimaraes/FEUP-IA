# Inside MenuBase.py
import pygame
import sys


class BaseMenu:
    def __init__(self, screen, screen_width, screen_height, background_image_path):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(None, 36)
        self.backColor = (255, 243, 228)
        self.yellow = (255, 190, 2)
        self.orange = (251, 90, 72)
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.click = False
        self.background_image = pygame.image.load(background_image_path).convert()
        self.background_image = pygame.transform.scale(self.background_image, (self.screen_width, self.screen_height))

    def draw_text(self, text, color, x, y):
        textobj = self.font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        self.screen.blit(textobj, textrect)

    def update_display(self):
        pygame.display.update()

    def handle_events(self):
        self.click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.click = True
