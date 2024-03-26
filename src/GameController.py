import sys

import pygame
from GameLogic import GameLogic
from GameView import GameView


# mode: 1 - Player vs Player, 2 - Player vs Computer, 3 - Computer vs Computer
# difficulty: 1 - Easy, 2 - Medium, 3 - Hard
class GameController:
    def __init__(self, width, height, mode=None, difficulty=None):
        self.width = width
        self.height = height
        self.mode = mode
        self.difficulty = difficulty
        self.board_size = 8
        self.game_logic = GameLogic(self.board_size)
        self.game_view = GameView(self.game_logic, width, height)
        self.clock = pygame.time.Clock()

    def get_cell_from_mouse_pos(self, mouse_pos):
        cell_size = self.width // self.board_size
        x, y = mouse_pos

        if x < self.width and y < self.height:
            col = x // cell_size
            row = y // cell_size
            return row, col
        else:
            return None, None

    def run(self):
        self.game_logic.initialize_board()
        valid_moves = []  # Store valid moves as a local variable
        selected_piece = None  # Use to track the currently selected piece
        winner = None  # Use to track the winner of the game
        game_ended = False
        placing_reserved = False  # Flag to indicate placing a reserved piece

        running = True
        while running:

            if (self.mode == 2 and self.game_logic.turn == 'R') or (self.mode == 3):
                self.game_logic.computer_move(1, self.game_view)
                self.game_logic.count_pieces()

                # Ensure all visual updates are processed
                self.game_view.draw_board()  # Redraw the board to reflect the new state
                self.game_view.draw_pieces()  # Redraw pieces
                self.game_view.draw_side_menu()  # Optionally update side menu if needed
                pygame.display.flip()  # Update the display to show the changes

                pygame.time.delay(1000)

                winner = self.game_logic.check_winner()
                if winner:
                    pygame.time.delay(1000)  # Additional delay to announce the winner

                    game_ended = True
                continue

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN and not game_ended:
                    mouse_pos = pygame.mouse.get_pos()
                    row, col = self.get_cell_from_mouse_pos(mouse_pos)

                    if placing_reserved:
                        if row is not None and col is not None:
                            success = self.game_logic.move_reserved_piece(row, col, self.game_logic.turn)
                            if success:
                                self.game_logic.count_pieces()
                                placing_reserved = False
                                winner = self.game_logic.check_winner()
                                print(winner)
                                if winner is not None:
                                    game_ended = True
                                    break
                                else:
                                    self.game_logic.switch_turns()
                            else:
                                print("Invalid move")
                        placing_reserved = False
                        continue

                    # Check if the reserved button was clicked
                    if hasattr(self.game_view, 'button_rect') and self.game_view.button_rect.collidepoint(mouse_pos):
                        if (self.game_logic.turn == 'B' and self.game_logic.blue_reserved > 0) or (
                                self.game_logic.turn == 'R' and self.game_logic.red_reserved > 0):
                            placing_reserved = True
                        continue

                    if row is not None and col is not None and not placing_reserved:
                        if selected_piece:
                            if (row, col) in valid_moves:
                                self.game_logic.move_stack(selected_piece, (row, col))
                                self.game_logic.count_pieces()
                                selected_piece = None  # Deselect piece after moving
                                valid_moves = []  # Clear valid moves after the piece has moved

                                winner = self.game_logic.check_winner()
                                if winner:
                                    game_ended = True
                                else:
                                    self.game_logic.switch_turns()
                            else:
                                selected_piece = None
                                valid_moves = []
                        else:
                            # Select a piece if it's the current player's turn
                            if self.game_logic.board[row][col] != 'N' and self.game_logic.board[row][
                                col] != 'X' and self.game_logic.turn == \
                                    self.game_logic.board[row][col][-1]:
                                selected_piece = (row, col)
                                valid_moves = self.game_logic.get_valid_moves_for_position(row, col)

            if not game_ended:
                if not placing_reserved:
                    self.game_view.screen.fill(self.game_view.BLACK)  # Clear the screen
                    self.game_view.draw_board()
                    self.game_view.draw_pieces()
                    self.game_view.draw_side_menu()
                if placing_reserved:
                    self.game_view.highlight_moves(
                        [(i, j) for i in range(self.game_logic.board_size) for j in range(self.game_logic.board_size) if
                         self.game_logic.board[i][j] != 'N'])
                elif selected_piece:
                    self.game_view.highlight_moves(valid_moves)

            else:
                if winner:
                    self.game_view.screen.fill(self.game_view.BLACK)
                    self.game_view.display_winner(winner)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    pygame.init()
    game_controller = GameController(600, 600, 2, 2)
    game_controller.run()
