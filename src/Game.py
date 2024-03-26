import random

import pygame
import sys

# will need to call game with mode 1 for player vs player, 2 for player vs computer, 3 for computer vs computer
# game = Game(600, 600, mode)

# will need to call game with difficulty 1 for easy, 2 for medium, 3 for hard (only for computers)
# game = Game(600, 600, 2, 3)
class Game:
    def __init__(self, width, height, mode=None, difficulty=None):
        self.mode = mode
        self.difficulty = difficulty
        self.button_rect = None
        self.red_reserved = 1
        self.blue_reserved = 1
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
        self.YELLOW = (255, 190, 2)
        self.font = pygame.font.Font(None, 36)
        self.turn = 'B'  # 'B' for blue, 'R' for red
        self.blue_pieces = 18
        self.red_pieces = 18
        self.selected_piece = None
        self.menu_width = 300
        self.total_width = width + self.menu_width
        self.screen = pygame.display.set_mode((self.total_width, height))  # Adjust screen size for side menu

    def initialize_board(self):
        # self.board = [
        #     ['N', 'N', 'X', 'X', 'X', 'X', 'N', 'N'],
        #     ['N', 'B', 'B', 'R', 'R', 'B', 'B', 'N'],
        #     ['X', 'R', 'R', 'B', 'B', 'R', 'R', 'X'],
        #     ['X', 'B', 'B', 'R', 'R', 'B', 'B', 'X'],
        #     ['X', 'R', 'R', 'B', 'B', 'R', 'R', 'X'],
        #     ['X', 'B', 'B', 'R', 'R', 'B', 'B', 'X'],
        #     ['N', 'R', 'R', 'B', 'B', 'R', 'R', 'N'],
        #     ['N', 'N', 'X', 'X', 'X', 'X', 'N', 'N']
        # ]

        self.board = [
            ['N', 'N', 'X', 'X', 'X', 'X', 'N', 'N'],
            ['N', 'X', 'B', 'R', 'R', 'X', 'X', 'N'],
            ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
            ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
            ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
            ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
            ['N', 'X', 'X', 'X', 'X', 'X', 'X', 'N'],
            ['N', 'N', 'X', 'X', 'X', 'X', 'N', 'N']
        ]

    # This function draws the board taking into consideration the board size. If piece in board is 'N', it will draw a
    # rectangle with the color of the background, otherwise, it will draw a rectangle with the color of the background
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

    # This function draws the pieces on the board. It takes into consideration the board size to calculate the size
    # of each piece and the position of each piece. It also draws a border around each piece to make it easier to see
    # the pieces on the board. If piece is 'B', it will draw a blue piece, if piece is 'R', it will draw a red piece,
    # otherwise it will draw nothing
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

    # This function draws the side menu. It takes into consideration the width of the screen and the height of the
    # screen. It also draws the text for the game title, the turn, the pieces in play, and the pieces reserved for each
    # player.
    def draw_side_menu(self):
        pygame.draw.rect(self.screen, self.WHITE, (self.width, 0, self.menu_width, self.height))
        self.draw_text('Focus Game', self.font, self.BLACK, self.width + 70, 20)
        self.draw_text('Turn:', self.font, self.BLACK, self.width + 120, 100)
        self.draw_text('Blue', self.font, self.BLUE if self.turn == 'B' else self.BLACK, self.width + 90, 130)
        self.draw_text('Red', self.font, self.RED if self.turn == 'R' else self.BLACK, self.width + 180, 130)
        self.draw_text('Pieces in Play:', self.font, self.BLACK, self.width + 70, 200)
        self.draw_text(str(self.blue_pieces), self.font, self.BLUE, self.width + 100, 230)
        self.draw_text(str(self.red_pieces), self.font, self.RED, self.width + 180, 230)
        self.draw_text('Pieces Reserved:', self.font, self.BLACK, self.width + 60, 300)
        self.draw_text(str(self.blue_reserved), self.font, self.BLUE, self.width + 100, 330)
        self.draw_text(str(self.red_reserved), self.font, self.RED, self.width + 180, 330)
        self.draw_reserved_button()

    # This function draws the text on the screen. It takes into consideration the text, the font, the color, and the
    # position of the text. It then renders the text and draws it on the screen
    def draw_text(self, text, font, color, x, y):
        text = font.render(text, 1, color)
        textrect = text.get_rect()
        textrect.topleft = (x, y)
        self.screen.blit(text, textrect)

    def draw_reserved_button(self):
        if (self.turn == 'B' and self.blue_reserved > 0) or (self.turn == 'R' and self.red_reserved > 0):
            # Calculate the button's position and size
            button_x = self.width + 50
            button_y = 400
            button_width = 200
            button_height = 50

            # Rectangle for the border - slightly larger than the button itself
            border_rect = pygame.Rect(button_x - 2, button_y - 2, button_width + 4, button_height + 4)

            # Draw the border rectangle
            pygame.draw.rect(self.screen, self.BLACK, border_rect)

            # Now draw the button rectangle on top of the border
            self.button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            pygame.draw.rect(self.screen, self.YELLOW, self.button_rect)

            # Adjust the text drawing position to center it in the button
            # You might need to adjust the text positioning based on your font size and button dimensions
            text_x = button_x + (button_width // 2)
            text_y = button_y + (button_height // 2) - 10  # Adjust based on your font's height
            self.draw_text('Play Reserved', self.font, self.WHITE, button_x + 20, button_y + 15)

    # This function gets the cell from the mouse position. It takes into consideration the mouse position and the
    # cell size. It then calculates the row and column of the cell based on the mouse position and the cell size. If
    # the mouse position is within the width and height of the screen, it returns the row and column of the cell,
    # otherwise it returns None, None
    def get_cell_from_mouse_pos(self, mouse_pos):
        cell_size = self.width // self.board_size
        x, y = mouse_pos

        if x < self.width and y < self.height:
            col = x // cell_size
            row = y // cell_size
            return row, col
        else:
            return None, None

    # This function gets the valid moves for a piece. It takes into consideration the row and column of the piece. It
    # then gets the stack from the board at the row and column. It then calculates the valid moves for the piece based
    # on the number of pieces in the stack and the directions to check. It then returns the valid moves for the piece
    def get_valid_moves(self, row, col):
        stack = self.board[row][col]
        valid_moves = []

        # Number of pieces in the stack determines the number of spaces you can move
        num_pieces = len(stack)

        # Define the directions to check: up, down, left, right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        # Check each direction
        for dr, dc in directions:
            for i in range(1, num_pieces + 1):
                new_row, new_col = row + dr * i, col + dc * i
                # Check if new position is within bounds
                if 0 <= new_row < self.board_size and 0 <= new_col < self.board_size:
                    # If the cell is not part of the board ('N'), it's not a valid move
                    if self.board[new_row][new_col] == 'N':
                        break
                    # Add the move if the space is either empty ('X'), contains opponent's piece on top,
                    # or contains player's own pieces
                    valid_moves.append((new_row, new_col))
                else:
                    # Out of bounds
                    break

        return valid_moves

    def get_all_valid_moves(self, player):
        valid_moves = []
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board[row][col][-1] == player:  # Check if the top piece belongs to the player
                    piece_valid_moves = self.get_valid_moves(row, col)
                    for move in piece_valid_moves:
                        valid_moves.append(
                            (row, col, move))  # Append the move as a tuple (from_row, from_col, to_row, to_col)
        return valid_moves

    # This function highlights the valid moves. It takes into consideration the valid moves. It then calculates the cell
    # size based on the width and the board size. It then draws a rectangle on the screen with the highlight color for
    # each valid move

    # TODO: Fix the highlight_moves function when placing piece, yellow border too thick
    def highlight_moves(self, valid_moves):
        cell_size = self.width // self.board_size
        for row, col in valid_moves:
            x = col * cell_size
            y = row * cell_size
            # Define a color for the highlight
            highlight_color = (255, 255, 0)  # Light blue for example

            # Draw a rectangle on the screen with the highlight color
            pygame.draw.rect(self.screen, highlight_color, (x, y, cell_size, cell_size),
                             5)  # 5 is the thickness of the border

    # This function switches the turns. It takes into consideration the current turn. If the current turn is 'R', it
    # switches the turn to 'B', otherwise it switches the turn to 'R'
    def switch_turns(self):
        self.turn = 'B' if self.turn == 'R' else 'R'

    # This function moves the piece. It takes into consideration the 'from' position and the 'to' position. It then
    # calculates the distance based on the 'from' position and the 'to' position. It then gets the stack from the board
    # at the 'from' position. It then calculates the number of pieces to move based on the distance. It then gets the
    # moving stack from the original position. It then calculates the number of pieces to move based on the distance.
    # It then determines
    def move_piece(self, from_pos, to_pos):
        print(f"Attempting to move from {from_pos} to {to_pos}")

        from_row, from_col = from_pos
        to_row, to_col = to_pos

        # Calculate the number of pieces to move based on the distance
        distance = abs(to_row - from_row) + abs(to_col - from_col)

        # Get the stack from the original position
        moving_stack = self.board[from_row][from_col]
        print(f"Board before move: {self.board[to_row][to_col]} moving stack: {moving_stack}")

        # The number of pieces to move is the same as the distance
        pieces_to_move = min(distance, len(moving_stack))
        moving_pieces = moving_stack[-pieces_to_move:]

        # Determine the player making the move
        player_moving = moving_pieces[-1]  # Assuming the moving piece is the last in the selected stack

        # Initialize capture and reserve counts for this move
        capture_count = 0
        reserve_count = 0

        # If the target cell is empty ('X'), just move the selected pieces
        if self.board[to_row][to_col] == 'X':
            self.board[to_row][to_col] = moving_pieces
        else:
            # Calculate the final stack considering the max stack size of 5
            destination_stack = self.board[to_row][to_col]
            total_length = len(destination_stack) + pieces_to_move

            # Identify the pieces to be removed and adjust capture/reserve counts
            if total_length > 5:
                # Determine the number of pieces that will be removed
                remove_count = total_length - 5

                # Remove pieces from the destination stack as needed
                for i in range(remove_count):
                    # Remove from the bottom of the destination stack
                    removed_piece = destination_stack[i]
                    if removed_piece != player_moving:
                        capture_count += 1  # The piece is different from the moving player's piece
                    else:
                        reserve_count += 1  # The piece belongs to the moving player

                # Trim the destination stack and add the moving pieces
                destination_stack = destination_stack[remove_count:]

            self.board[to_row][to_col] = destination_stack + moving_pieces

        # Remove the moved pieces from the original stack
        self.board[from_row][from_col] = self.board[from_row][from_col][:-pieces_to_move]
        if not self.board[from_row][from_col]:
            # If no pieces remain, mark the original position as empty
            self.board[from_row][from_col] = 'X'

        # Update capture and reserve counts based on the player
        if player_moving == 'B':
            self.blue_reserved += reserve_count
            self.red_pieces -= capture_count
        else:
            self.red_reserved += reserve_count
            self.blue_pieces -= capture_count

        print(f"Board after move: {self.board[to_row][to_col]}")
        print(f"Blue reserved: {self.blue_reserved}, Red reserved: {self.red_reserved}")
        print(f"Blue pieces: {self.blue_pieces}, Red pieces: {self.red_pieces}")

    def check_winner(self):
        # Assume initially that both players can move
        can_move = {'B': False, 'R': False}

        # Check the board for potential moves for each player
        for row in range(self.board_size):
            for col in range(self.board_size):
                stack = self.board[row][col]
                if stack == 'X' or stack == 'N':  # Skip empty spaces and non-playable areas
                    continue

                top_piece = stack[-1]  # The top-most piece of the stack
                # Check if the current player has a potential move
                if self.get_valid_moves(row, col):
                    can_move[top_piece] = True

        # Determine the loser based on potential moves and reserved pieces
        loser = None
        for player in ['B', 'R']:
            if not can_move[player]:
                if (player == 'B' and self.blue_reserved == 0) or (player == 'R' and self.red_reserved == 0):
                    loser = player
                    break

        # If we have identified a loser, return the winner
        if loser:
            return 'R' if loser == 'B' else 'B'
        else:
            return None  # Game continues

    def place_reserved_piece(self, row, col, player):
        print(f"Placing reserved piece for {player} at {row}, {col}")

        capture_count = 0
        reserve_count = 0

        # if i click on something outside the board
        if row is None or col is None:
            return False
        # Only allow placing a piece if the cell is empty ('X') or already contains pieces (a list).
        elif self.board[row][col] == 'X':
            # If the cell is empty, initialize a new list with the player's piece.
            self.board[row][col] = player
        elif self.board[row][col] != 'X' and self.board[row][col] != 'N':
            # Calculate the final stack considering the max stack size of 5
            destination_stack = self.board[row][col]
            total_length = len(destination_stack) + 1

            # Identify the pieces to be removed and adjust capture/reserve counts
            if total_length > 5:
                # Determine the number of pieces that will be removed
                remove_count = total_length - 5

                # Remove pieces from the destination stack as needed
                for i in range(remove_count):

                    # Remove from the bottom of the destination stack
                    removed_piece = destination_stack[i]
                    if removed_piece != player:
                        capture_count += 1  # The piece is different from the moving player's piece
                    else:
                        reserve_count += 1  # The piece belongs to the moving player

                    # Trim the destination stack and add the moving pieces
                    destination_stack = destination_stack[remove_count:]

            self.board[row][col] = destination_stack + player
            # Remove the moved pieces from the original stack

            # Update capture and reserve counts based on the player
            print(f"Board after move: {self.board[row][col]}")
            print(f"Blue reserved: {self.blue_reserved}, Red reserved: {self.red_reserved}")
            print(f"Blue pieces: {self.blue_pieces}, Red pieces: {self.red_pieces}")
        else:
            print("unexpected")
            return False

        if player == 'B' and self.blue_reserved > 0:
            self.blue_reserved += reserve_count - 1
            self.red_pieces -= capture_count
        elif player == 'R' and self.red_reserved > 0:
            self.red_reserved += reserve_count - 1
            self.blue_pieces -= capture_count
        else:
            # In case there's an attempt to place a piece without having any reserved, return False.
            return False

        return True  # Indicate success.

    import random

    def computer_move(self, difficulty):

        # easy - random move
        if difficulty == 1:
            valid_moves = self.get_all_valid_moves('R')  # Get ALL valid moves for the computer player (Red)
            if not valid_moves and self.red_reserved == 0: # If no valid moves and no reserved pieces
                print("No valid moves available")
                return

            if valid_moves: # If there are valid moves, select a random move
                from_row, from_col, (to_row, to_col) = random.choice(valid_moves)
                print(f"Computer moves from {from_row}, {from_col} to {to_row}, {to_col}")
                self.move_piece((from_row, from_col), (to_row, to_col))

            elif self.red_reserved > 0: # If no valid moves but there are reserved pieces
                # select random move in board
                to_row, to_col = random.choice([(i, j) for i in range(self.board_size) for j in range(self.board_size) if self.board[i][j] != 'N'])
                self.place_reserved_piece(to_row, to_col, 'R')

        elif difficulty == 2:
            # Placeholder for Monte Carlo Tree Search
            pass
        elif difficulty == 3:
            # Placeholder for Minimax algorithm
            pass

        self.switch_turns()  # Switch turns at the end of the computer move

    def run(self):
        self.initialize_board()
        valid_moves = []  # Store valid moves as a local variable
        selected_piece = None  # Use to track the currently selected piece
        winner = None  # Use to track the winner of the game
        game_ended = False
        placing_reserved = False  # Flag to indicate placing a reserved piece

        running = True
        while running:

            if (self.mode == 2 and self.turn == 'R') or (self.mode == 3):
                self.computer_move(1)
                # Continue to the next iteration to avoid processing player input
                continue

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN and not game_ended:
                    mouse_pos = pygame.mouse.get_pos()
                    row, col = self.get_cell_from_mouse_pos(mouse_pos)

                    # If placing_reserved is True, try to place a reserved piece
                    if placing_reserved:
                        if row is not None and col is not None:
                            success = self.place_reserved_piece(row, col, self.turn)
                            if success:
                                placing_reserved = False  # Reset the flag after placing
                                winner = self.check_winner()
                                print(winner)
                                if winner is not None:
                                    game_ended = True
                                    break
                                else:
                                    self.switch_turns()
                            else:
                                print("Invalid move")
                        placing_reserved = False  # Reset the flag if the move was invalid
                        continue  # Skip the rest of this iteration

                    # Check if the reserved button was clicked
                    if hasattr(self, 'button_rect') and self.button_rect.collidepoint(mouse_pos):
                        if (self.turn == 'B' and self.blue_reserved > 0) or (
                                self.turn == 'R' and self.red_reserved > 0):
                            placing_reserved = True
                            self.highlight_moves([(i, j) for i in range(self.board_size) for j in range(self.board_size)])
                            continue

                    # Check if a piece is selected and if the click is within bounds
                    if row is not None and col is not None and not placing_reserved:
                        if selected_piece:
                            # Attempt to move the selected piece
                            if (row, col) in valid_moves:
                                self.move_piece(selected_piece, (row, col))
                                selected_piece = None  # Deselect piece after moving
                                valid_moves = []  # Clear valid moves after the piece has moved

                                winner = self.check_winner()
                                if winner:
                                    game_ended = True
                                else:
                                    self.switch_turns()
                            else:
                                # Deselect if clicked outside valid moves
                                selected_piece = None
                                valid_moves = []
                        else:
                            # Select a piece if it's the current player's turn
                            if self.board[row][col] != 'N' and self.board[row][col] != 'X' and self.turn == \
                                    self.board[row][col][-1]:
                                selected_piece = (row, col)
                                valid_moves = self.get_valid_moves(row, col)

            if not game_ended:
                if not placing_reserved:
                    self.screen.fill(self.BLACK)  # Clear the screen
                self.draw_board()
                self.draw_pieces()
                if placing_reserved:
                    self.highlight_moves([(i, j) for i in range(self.board_size) for j in range(self.board_size) if
                                          self.board[i][j] != 'N'])
                elif selected_piece:
                    self.highlight_moves(valid_moves)
                self.draw_side_menu()
            else:
                if winner:
                    self.screen.fill(self.BLACK)
                    self.display_winner(winner)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

    def display_winner(self, winner):
        winner_text = f"Winner is {'Blue' if winner == 'B' else 'Red'}!"
        self.draw_text(winner_text, self.font, self.WHITE, self.width // 2, self.height // 2)


if __name__ == "__main__":
    pygame.init()
    game = Game(600, 600, 2, 3)
    game.run()
