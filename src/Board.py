import pygame
import sys


class Board:
    def __init__(self, width, height):
        self.board = None
        self.board_size = 8
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
        self.font = pygame.font.Font(None, 36)
        self.turn = 'B'  # 'B' for blue, 'R' for red
        self.selected_piece = None
        self.message_timer = None
        self.message_text = None
        self.menu_width = 300
        self.total_width = width + self.menu_width
        self.screen = pygame.display.set_mode((self.total_width, height))  # Adjust screen size for side menu

    def initialize_board(self):
        self.board = [
            ['N', 'N', 'X', 'X', 'X', 'X', 'N', 'N'],
            ['N', 'B', 'B', 'R', 'R', 'B', 'B', 'N'],
            ['X', 'R', 'R', 'B', 'B', 'R', 'R', 'X'],
            ['X', 'B', 'B', 'R', 'R', 'B', 'B', 'X'],
            ['X', 'R', 'R', 'B', 'B', 'R', 'R', 'X'],
            ['X', 'B', 'B', 'R', 'R', 'B', 'B', 'X'],
            ['N', 'R', 'R', 'B', 'B', 'R', 'R', 'N'],
            ['N', 'N', 'X', 'X', 'X', 'X', 'N', 'N']
        ]

    def draw_board(self):
        self.screen.fill(self.GRAY)
        cell_size = self.width // self.board_size

        line_color = self.BLACK
        space_color = self.WHITE

        for j in range(self.board_size):
            for i in range(self.board_size):
                x = i * cell_size
                y = j * cell_size

                if self.board[j][i] == 'N':
                    color = self.screen.get_at((x, y))
                else:
                    color = space_color

                pygame.draw.rect(self.screen, color, (x, y, cell_size, cell_size))

                if not self.board[j][i] == 'N':
                    pygame.draw.rect(self.screen, line_color, (x, y, cell_size, cell_size), 1)

    def draw_pieces(self):
        cell_size = self.width // len(self.board[0])
        piece_height = cell_size // 6  # Set the height of each piece
        piece_width = cell_size * 0.8  # Set the width of each piece, slightly less than cell size for padding

        for j in range(len(self.board)):
            for i in range(len(self.board[0])):
                stack = self.board[j][i]
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

    def run(self):
        self.initialize_board()

        running = True
        while running:
            self.draw_board()
            self.draw_pieces()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    pygame.init()
    game = Board(600, 600)
    game.run()
