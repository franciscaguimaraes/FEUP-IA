import pygame


class GameView:
    def __init__(self, game_logic, width, height):
        self.game_logic = game_logic
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Focus Game")
        self.clock = pygame.time.Clock()
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GRAY = (200, 200, 200)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)
        self.GREEN = (0, 255, 0)
        self.YELLOW = (255, 190, 2)
        self.font = pygame.font.Font(None, 36)
        self.menu_width = 300
        self.button_rect = pygame.Rect(0, 0, 0, 0)
        self.total_width = width + self.menu_width
        self.screen = pygame.display.set_mode((self.total_width, height))

    def draw_board(self):
        self.screen.fill(self.GRAY)
        board_size = self.game_logic.board_size
        cell_size = self.width // board_size

        line_color = self.BLACK
        space_color = self.WHITE

        for j in range(board_size):
            for i in range(board_size):
                x = i * cell_size
                y = j * cell_size

                if self.game_logic.board[j][i] == 'N':
                    color = self.screen.get_at((x, y))
                else:
                    color = space_color

                pygame.draw.rect(self.screen, color, (x, y, cell_size, cell_size))

                if not self.game_logic.board[j][i] == 'N':
                    pygame.draw.rect(self.screen, line_color, (x, y, cell_size, cell_size), 1)

    def draw_pieces(self):
        board = self.game_logic.board
        cell_size = self.width // len(board[0])
        piece_height = cell_size // 6  # Set the height of each piece
        piece_width = cell_size * 0.8  # Set the width of each piece, slightly less than cell size for padding

        for j in range(len(board)):
            for i in range(len(board[0])):
                stack = board[j][i]
                if stack:
                    stack_height = len(stack)
                    x = i * cell_size + (cell_size - piece_width) // 2  # Center the stack in the cell
                    y = j * cell_size + cell_size - piece_height  # Start from the bottom of the cell

                    for k in range(min(stack_height, 5)):
                        color = self.BLUE if stack[k] == 'B' else self.RED if stack[k] == 'R' else None
                        if color:
                            pygame.draw.rect(self.screen, color, (x, y - k * piece_height, piece_width, piece_height))
                            pygame.draw.rect(self.screen, self.BLACK,
                                             (x, y - k * piece_height, piece_width, piece_height), 1)  # Draw border

    def draw_side_menu(self):
        pygame.draw.rect(self.screen, self.WHITE, (self.width, 0, self.menu_width, self.height))
        self.draw_text('Focus Game', self.font, self.BLACK, self.width + 70, 20)
        self.draw_text('Turn:', self.font, self.BLACK, self.width + 120, 100)
        self.draw_text('Blue', self.font, self.BLUE if self.game_logic.turn == 'B' else self.BLACK, self.width + 90,
                       130)
        self.draw_text('Red', self.font, self.RED if self.game_logic.turn == 'R' else self.BLACK, self.width + 180, 130)
        self.draw_text('Pieces in Play:', self.font, self.BLACK, self.width + 70, 200)
        self.draw_text(str(self.game_logic.blue_pieces), self.font, self.BLUE, self.width + 100, 230)
        self.draw_text(str(self.game_logic.red_pieces), self.font, self.RED, self.width + 180, 230)
        self.draw_text('Pieces Reserved:', self.font, self.BLACK, self.width + 60, 300)
        self.draw_text(str(self.game_logic.blue_reserved), self.font, self.BLUE, self.width + 100, 330)
        self.draw_text(str(self.game_logic.red_reserved), self.font, self.RED, self.width + 180, 330)
        self.draw_reserved_button()

    def draw_text(self, text, font, color, x, y):
        text = font.render(text, 1, color)
        textrect = text.get_rect()
        textrect.topleft = (x, y)
        self.screen.blit(text, textrect)

    def draw_reserved_button(self):
        if (self.game_logic.turn == 'B' and self.game_logic.blue_reserved > 0) or (self.game_logic.turn == 'R'
                                                                                   and self.game_logic.red_reserved > 0):
            button_x = self.width + 50
            button_y = 400
            button_width = 200
            button_height = 50

            border_rect = pygame.Rect(button_x - 2, button_y - 2, button_width + 4, button_height + 4)
            pygame.draw.rect(self.screen, self.BLACK, border_rect)
            self.button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            pygame.draw.rect(self.screen, self.YELLOW, self.button_rect)

            self.draw_text('Play Reserved', self.font, self.WHITE, button_x + 20, button_y + 15)

    def display_winner(self, winner):
        winner_text = f"Winner is {'Blue' if winner == 'B' else 'Red'}!"
        self.draw_text(winner_text, self.font, self.WHITE, self.width // 2, self.height // 2)

    def highlight_moves(self, valid_moves):
        cell_size = self.width // self.game_logic.board_size
        for row, col in valid_moves:
            x = col * cell_size
            y = row * cell_size

            highlight_color = (255, 255, 0)

            pygame.draw.rect(self.screen, highlight_color, (x, y, cell_size, cell_size), 5)