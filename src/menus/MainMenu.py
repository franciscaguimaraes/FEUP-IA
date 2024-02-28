# Inside MainMenu.py
import pygame
import sys


class MainMenu:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.font = pygame.font.Font(None, 36)
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.backColor = (255, 243, 228)
        self.yellow = (255, 190, 2)
        self.click = False
        self.background_image = pygame.image.load('./imgs/menuBackground.png').convert()
        self.background_image = pygame.transform.scale(self.background_image, (self.screen_width, self.screen_height))

    def draw_text(self, text, font, color, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        self.screen.blit(textobj, textrect)

    def run(self):
        while True:
            self.screen.blit(self.background_image, (0, 0))
            mx, my = pygame.mouse.get_pos()

            button_1 = pygame.Rect(70, 500, 250, 50) # posx, posy, largura, altura
            button_2 = pygame.Rect(70, 560, 250, 50)
            button_3 = pygame.Rect(70, 620, 250, 50)

            if button_1.collidepoint((mx, my)):
                if self.click:
                    self.start_game()
            if button_2.collidepoint((mx, my)):
                if self.click:
                    self.high_scores()
            if button_3.collidepoint((mx, my)):
                if self.click:
                    pygame.quit()
                    sys.exit()

            pygame.draw.rect(self.screen, self.yellow, button_1)
            pygame.draw.rect(self.screen, self.yellow, button_2)
            pygame.draw.rect(self.screen, self.yellow, button_3)

            self.draw_text('Start Game', self.font, self.backColor, 90, 510)
            self.draw_text('Instructions', self.font, self.backColor, 90, 570)
            self.draw_text('Exit', self.font, self.backColor, 90, 630)

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

            pygame.display.update()

    def start_game(self):
        print("Start game placeholder")

    def high_scores(self):
        print("High scores placeholder")
