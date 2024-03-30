# mode: 1 - Player vs Player, 2 - Player vs Computer, 3 - Computer vs Computer
# difficulty: 1 - Easy, 2 - Medium, 3 - Hard, 4 - Expert
import sys

import pygame
from GameLogic import GameLogic
from GameView import GameView


class GameController:
    """ Initializes the game controller with settings for the game.
        @param width: The width of the game window in pixels.
        @param height: The height of the game window in pixels.
        @param board_size: The size of the game board (number of cells in width and height).
        @param mode: The game mode (1: Player vs Player, 2: Player vs Computer, 3: Computer vs Computer).
        @param difficulty1: The difficulty level for the first player (or only player in PvC mode).
        @param difficulty2: The difficulty level for the second player (in CvC mode).
        @param turn: The starting player ('B' for Blue, 'R' for Red).
    """

    def __init__(self, width, height, board_size=8, mode=None, difficulty1=None, difficulty2=None, turn='B'):
        self.width, self.height = width, height
        self.mode, self.difficulty1, self.difficulty2 = mode, difficulty1, difficulty2
        self.board_size = board_size
        self.game_logic = GameLogic(self.board_size, mode)
        self.game_view = GameView(self.game_logic, self.width, self.height)
        self.game_view.mode = mode
        self.game_view.difficulty1 = difficulty1
        self.game_view.difficulty2 = difficulty2
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_ended = False
        self.valid_moves = []
        self.selected_piece = None
        self.placing_reserved = False
        self.winner = None
        self.last_move_time = None
        self.game_logic.turn = turn  # Set the starting player color, human player always starts

    """ The main loop of the game. Handles game updates, event handling, and rendering until the game ends.
    """
    def run(self):
        while self.running:
            self.game_logic.count_pieces()
            self.handle_events()
            self.update_game_state()
            self.game_logic.count_pieces()
            self.render()
            self.clock.tick(60)

        self.cleanup()

    """ Checks if the reserved button is clicked.
        @param mouse_pos: The position of the mouse click.
        @return: True if the reserved button is clicked, False otherwise.
    """
    def check_reserved_button(self, mouse_pos):
        if self.game_logic.player == 'computer':
            return False
        elif self.game_logic.player == 'human':
            if hasattr(self.game_view, 'button_rect') and self.game_view.button_rect.collidepoint(mouse_pos):
                if (self.game_logic.turn == 'B' and self.game_logic.blue_reserved > 0) or (
                        self.game_logic.turn == 'R' and self.game_logic.red_reserved > 0):
                    self.placing_reserved = True
                return True
        return False

    """ Handles all events captured by pygame, such as quitting the game or mouse clicks.
    """
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not self.game_ended:
                self.handle_mouse_click()

    """ Handles mouse click events within the game, determining actions based on game state and click location.
    """
    def handle_mouse_click(self):
        mouse_pos = pygame.mouse.get_pos()

        if self.check_reserved_button(mouse_pos):
            return

        row, col = self.get_cell_from_mouse_pos(mouse_pos)

        if self.placing_reserved:
            success = self.handle_reserved_placement(row, col)
            self.placing_reserved = False
            if success:
                self.game_view.draw_everything(self.valid_moves, self.selected_piece, self.placing_reserved)
                pygame.display.flip()
        else:
            # if clicked out of bounds or on an invalid piece, do nothing
            if row is None or col is None:
                return
            self.handle_piece_selection_or_movement(row, col)
            self.game_view.draw_everything(self.valid_moves, self.selected_piece, self.placing_reserved)
            pygame.display.flip()

    """ Handles the placement of a reserved piece onto the board.
        @param row: The row where the piece is to be placed.
        @param col: The column where the piece is to be placed.
        @return: True if the placement was successful, False otherwise.
    """
    def handle_reserved_placement(self, row, col):
        if row is not None and col is not None:
            success = self.game_logic.move_reserved_piece((row, col), self.game_logic.turn)
            if success:
                winner = self.game_logic.check_winner()
                if winner:
                    self.game_ended = True
                    self.winner = winner
                else:
                    self.game_logic.switch_turns()
            else:
                print("Invalid move")
            return success

    """ Handles the selection of a piece or the movement of a selected piece.
        @param row: The row of the selected or target cell.
        @param col: The column of the selected or target cell.
    """
    def handle_piece_selection_or_movement(self, row, col):
        if self.selected_piece:
            if (row, col) in self.valid_moves:
                self.game_logic.move_stack(self.selected_piece, (row, col))
                self.selected_piece = None  # Deselect piece after moving
                self.valid_moves = []

                winner = self.game_logic.check_winner()
                if winner:
                    self.game_ended = True
                    self.winner = winner
                else:
                    self.game_logic.switch_turns()
            else:
                self.selected_piece = None
                self.valid_moves = []
        else:
            # Select a piece if it's the current player's turn and the piece belongs to them
            if (self.game_logic.board[row][col] != 'N' and
                    self.game_logic.board[row][col] != 'X' and
                    self.game_logic.turn == self.game_logic.board[row][col][-1]):
                self.selected_piece = (row, col)
                self.valid_moves = self.game_logic.get_valid_moves_for_position(row, col)

    """ Updates the game state, including checking for and handling computer moves in PvC or CvC modes.
    """
    def update_game_state(self):
        if self.mode == 2 and self.game_logic.player == 'computer':
            self.game_view.draw_everything(self.valid_moves, self.selected_piece, self.placing_reserved)
            self.handle_computer_move()

        elif self.mode == 3:
            self.game_view.draw_everything(self.valid_moves, self.selected_piece, self.placing_reserved)
            self.handle_computer_move()

        if not self.game_ended:
            self.check_for_winner()

    """ Handles the logic for computer moves, including determining moves based on the mode and difficulty settings.
    """
    def handle_computer_move(self):

        if self.mode == 2:
            self.game_logic.computer_move(self.mode, self.game_view, self.difficulty1, None)
        elif self.mode == 3:
            self.game_logic.computer_move(self.mode, self.game_view, self.difficulty1, self.difficulty2)

        pygame.time.delay(1000)
        self.game_logic.switch_turns()

    """ Checks if there's a winner and updates the game state accordingly.
    """
    def check_for_winner(self):
        self.winner = self.game_logic.check_winner()
        if self.winner:
            self.game_ended = True

    """ Renders the current state of the game to the display.
    """
    def render(self):
        self.game_view.draw_everything(self.valid_moves, self.selected_piece, self.placing_reserved)

        if self.game_ended:
            self.game_view.display_winner(self.winner)
            pygame.time.delay(5000)  # Delay before closing
            self.running = False

        pygame.display.flip()

    """ Converts mouse position to cell coordinates on the board.
        @param mouse_pos: The position of the mouse click.
        @return: A tuple (row, col) representing the cell under the mouse. Returns (None, None) if outside the board.
    """
    def get_cell_from_mouse_pos(self, mouse_pos):
        cell_size = self.width // self.board_size
        x, y = mouse_pos

        if x < self.width and y < self.height:
            col = x // cell_size
            row = y // cell_size
            return row, col
        else:
            return None, None

    """ Cleans up resources and exits the game.
    """
    def cleanup(self):
        pygame.quit()
        sys.exit()