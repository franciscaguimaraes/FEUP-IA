import random

import pygame


class GameView:
    """ Initializes the GameView with the game logic, dimensions for the game board, and graphical settings.
        @param game_logic: An instance of the game's logic class to interface with the game's mechanics.
        @param width: The width of the game board in pixels.
        @param height: The height of the game board in pixels.
    """

    def __init__(self, game_logic, width, height):
        self.game_logic = game_logic
        self.mode = None
        self.difficulty1 = None
        self.difficulty2 = None
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

    """ Draws the game board based on the current state of the game logic.
        Each cell of the board is drawn, and the colors of cells are updated according to their state. 
    """

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

    """ Draws the pieces on the board according to their positions in the game logic.
        Different colors represent different player pieces, and the pieces are stacked within the cells.
    """

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

    """Draws the side menu next to the game board. This menu includes game information such as the current player's 
    turn, the number of pieces in play, and buttons for game actions like playing a reserved piece.
    """

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
        # self.display_hint()

        small_font = pygame.font.Font(None, 23)  # smaller size

        if self.difficulty1 == 1:
            self.difficulty1 = 'Easy'
        elif self.difficulty1 == 2:
            self.difficulty1 = 'Medium'
        elif self.difficulty1 == 3:
            self.difficulty1 = 'Hard'
        elif self.difficulty1 == 4:
            self.difficulty1 = 'Expert'

        if self.difficulty2 == 1:
            self.difficulty2 = 'Easy'
        elif self.difficulty2 == 2:
            self.difficulty2 = 'Medium'
        elif self.difficulty2 == 3:
            self.difficulty2 = 'Hard'
        elif self.difficulty1 == 4:
            self.difficulty1 = 'Expert'

        if self.mode == 1:
            self.draw_text('Mode: Player vs Player', small_font, self.BLACK, self.width + 20, 530)
        elif self.mode == 2:
            self.draw_text('Mode: Player vs Computer', small_font, self.BLACK, self.width + 20, 530)
            self.draw_text(f'Difficulty: {self.difficulty1}', small_font, self.BLACK, self.width + 20, 560)
        elif self.mode == 3:
            self.draw_text('Mode: Computer vs Computer', small_font, self.BLACK, self.width + 20, 500)
            self.draw_text(f'Difficulty Computer Blue: {self.difficulty1}', small_font, self.BLACK, self.width + 20, 530)
            self.draw_text(f'Difficulty Computer Red: {self.difficulty2}', small_font, self.BLACK, self.width + 20, 550)

    """ Draws text into the game screen.
        @param text: The text string to display.
        @param font: The pygame font object to use for rendering the text.
        @param color: The color of the text.
        @param x: The x-coordinate of the top-left corner of the text.
        @param y: The y-coordinate of the top-left corner of the text.
    """

    def draw_text(self, text, font, color, x, y):
        text = font.render(text, 1, color)
        textrect = text.get_rect()
        textrect.topleft = (x, y)
        self.screen.blit(text, textrect)

    """ Draws the button for playing a reserved piece if the current player has any reserved pieces available.
        This button is only interactive and visible if the conditions are met.
    """

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

    """ Displays the winner of the game by loading and showing an image representing the winning player.
        @param winner: A string indicating the winner ('B' for Blue, 'R' for Red).
    """
    def display_winner(self, winner):
        # Select the correct image path based on the winner
        if winner == 'B':
            winner_image_path = 'imgs/winner_blue.png'
        else:
            winner_image_path = 'imgs/winner_red.png'
        try:
            winner_image = pygame.image.load(winner_image_path)
            # Scale the image to fit the screen
            # Here, we use self.total_width because it accounts for the side menu width as well
            winner_image = pygame.transform.scale(winner_image, (self.total_width, self.height))

            # Since the image now exactly matches the screen dimensions, start drawing from the top-left corner
            self.screen.blit(winner_image, (0, 0))
        except pygame.error as e:
            print(f"Error loading the winner image: {e}")

        pygame.display.flip()  # Update the full display Surface to the screen

    """ Highlights the cells on the board where the current player can move or place a piece.
        @param valid_moves: A list of tuples indicating the valid moves available.
        @param reserved: A boolean flag indicating whether the highlighting is for placing a reserved piece.
    """
    def highlight_moves(self, valid_moves, reserved=False):

        if reserved:
            width = 2
        else:
            width = 5

        cell_size = self.width // self.game_logic.board_size

        for row, col in valid_moves:
            x = col * cell_size
            y = row * cell_size

            highlight_color = (255, 255, 0)

            pygame.draw.rect(self.screen, highlight_color, (x, y, cell_size, cell_size), width)

    """ Central method to redraw the entire game screen, including the board, pieces, side menu, and any highlights.
        @param valid_moves: Optional. A list of valid moves if a piece is selected.
        @param selected_piece: Optional. Indicates if a piece is currently selected.
        @param placing_reserved: Optional. Indicates if placing a reserved piece is the current action.
    """
    def draw_everything(self, valid_moves=None, selected_piece=None, placing_reserved=False):
        self.screen.fill(self.BLACK)
        self.draw_board()
        self.draw_pieces()
        self.draw_side_menu()

        if selected_piece:
            self.highlight_moves(valid_moves, reserved=False)

        if placing_reserved:
            self.highlight_moves([(i, j) for i in range(self.game_logic.board_size)
                                  for j in range(self.game_logic.board_size)
                                  if self.game_logic.board[i][j] != 'N'], reserved=True)

        pygame.display.flip()  # Update the screen with everything drawn

    """ Optionally prints a hint to the console. This feature is not directly related to the game's GUI.
        @param display_hint: A boolean flag to control the display of the hint. If True, a hint is printed to the console.
    """
    def display_hint(self, display_hint=False):
        if display_hint:
            print("Displaying hint")

            hints = [
                "As the game nears its end, consider gathering reserve pieces. These are valuable and can lead to a win.",
                "Watch for stacks five pieces high under your opponent's control, with one of your pieces at the bottom. Adding one of your pieces on top lets you control the stack and earn a reserve piece.",
                "At the start of the game, aim to create many stacks that are two pieces high. Position these stacks two spaces apart in rows that meet, so you can easily combine them into a larger stack under your control.",
                "Avoid moving next to two or three of your opponent's single pieces. These are a threat because they're only one move away from taking over a stack."
            ]

            hint = random.choice(hints)
