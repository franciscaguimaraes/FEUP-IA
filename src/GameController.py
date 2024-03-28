# mode: 1 - Player vs Player, 2 - Player vs Computer, 3 - Computer vs Computer
# difficulty: 1 - Easy, 2 - Medium, 3 - Hard
import sys

import pygame
from GameLogic import GameLogic
from GameView import GameView


class GameController:
    def __init__(self, width, height, board_size=8, mode=None, difficulty1=None, difficulty2=None, turn='B'):
        self.width, self.height = width, height
        self.mode, self.difficulty1, self.difficulty2 = mode, difficulty1, difficulty2
        self.board_size = board_size
        self.game_logic = GameLogic(self.board_size)
        self.game_view = GameView(self.game_logic, self.width, self.height)
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_ended = False
        self.valid_moves = []
        self.selected_piece = None
        self.placing_reserved = False
        self.winner = None
        self.last_move_time = None
        self.game_logic.turn = turn # Set the starting player color, human player always starts

    def run(self):
        while self.running:
            self.game_logic.count_pieces()
            self.handle_events()
            self.update_game_state()
            self.game_logic.count_pieces()
            self.render()
            self.clock.tick(60)

        self.cleanup()

    def check_reserved_button(self, mouse_pos):
        if hasattr(self.game_view, 'button_rect') and self.game_view.button_rect.collidepoint(mouse_pos):
            if (self.game_logic.turn == 'B' and self.game_logic.blue_reserved > 0) or (
                    self.game_logic.turn == 'R' and self.game_logic.red_reserved > 0):
                self.placing_reserved = True
            return True
        return False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not self.game_ended:
                self.handle_mouse_click()

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
            self.handle_piece_selection_or_movement(row, col)
            self.game_view.draw_everything(self.valid_moves, self.selected_piece, self.placing_reserved)
            pygame.display.flip()

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
            # if clicked out of bounds or on an invalid piece, do nothing
            if row is None or col is None:
                return
            # Select a piece if it's the current player's turn and the piece belongs to them
            if (self.game_logic.board[row][col] != 'N' and
                    self.game_logic.board[row][col] != 'X' and
                    self.game_logic.turn == self.game_logic.board[row][col][-1]):
                self.selected_piece = (row, col)
                self.valid_moves = self.game_logic.get_valid_moves_for_position(row, col)

    def update_game_state(self):
        if self.mode is 2 and self.game_logic.player == 'computer':
            self.game_view.draw_everything(self.valid_moves, self.selected_piece, self.placing_reserved)
            self.handle_computer_move()

        elif self.mode == 3:
            self.game_view.draw_everything(self.valid_moves, self.selected_piece, self.placing_reserved)
            self.handle_computer_move()

        if not self.game_ended:
            self.check_for_winner()

    def handle_computer_move(self):

        if self.mode == 2:
            self.game_logic.computer_move(self.mode, self.game_view, self.difficulty1, None)
        elif self.mode == 3:
            self.game_logic.computer_move(self.mode, self.game_view, self.difficulty1, self.difficulty2)

        pygame.time.delay(1000)
        self.game_logic.switch_turns()

    def check_for_winner(self):
        self.winner = self.game_logic.check_winner()
        if self.winner:
            self.game_ended = True

    def render(self):
        self.game_view.draw_everything(self.valid_moves, self.selected_piece, self.placing_reserved)

        if self.game_ended:
            self.game_view.display_winner(self.winner)
            pygame.time.delay(5000)  # Delay before closing
            self.running = False

        pygame.display.flip()

    def get_cell_from_mouse_pos(self, mouse_pos):
        cell_size = self.width // self.board_size
        x, y = mouse_pos

        if x < self.width and y < self.height:
            col = x // cell_size
            row = y // cell_size
            return row, col
        else:
            return None, None

    def cleanup(self):
        pygame.quit()
        sys.exit()