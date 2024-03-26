import random

import pygame


class GameLogic:
    def __init__(self, board_size):
        self.board_size = board_size
        self.board = None
        self.initialize_board()
        self.turn = 'B'  # Blue player goes first later this decision will be passed as an argument
        self.blue_reserved = 0
        self.red_reserved = 0
        self.blue_pieces = None
        self.red_pieces = None

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

        self.count_pieces()

    def count_pieces(self):
        self.blue_pieces = 0
        self.red_pieces = 0
        for row in self.board:
            for cell in row:
                if cell in ['N', 'X']:
                    continue
                self.blue_pieces += cell.count('B')
                self.red_pieces += cell.count('R')

    def get_valid_moves_for_position(self, row, col):
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

    def get_valid_moves_for_player(self, player):
        valid_moves = []
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board[row][col][-1] == player:  # Check if the top piece belongs to the player
                    piece_valid_moves = self.get_valid_moves_for_position(row, col)
                    for move in piece_valid_moves:
                        valid_moves.append(
                            (row, col, move))  # Append the move as a tuple (from_row, from_col, to_row, to_col)
        return valid_moves

    def move_stack(self, from_pos, to_pos):
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

    def move_reserved_piece(self, row, col, player):
        print(f"Placing reserved piece for {player} at {row}, {col}")

        capture_count = 0
        reserve_count = 0

        # if I click on something outside the board
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
                if self.get_valid_moves_for_position(row, col):
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

    def switch_turns(self):
        self.turn = 'B' if self.turn == 'R' else 'R'

    def computer_move(self, difficulty, game_view):
        # easy - random move
        if difficulty == 1:
            valid_moves = self.get_valid_moves_for_player('R')  # Get ALL valid moves for the computer player (Red)

            if not valid_moves and self.red_reserved == 0:  # If no valid moves and no reserved pieces
                print("No valid moves available")
                return

            if valid_moves:  # If there are valid moves, select a random move
                from_row, from_col, (to_row, to_col) = random.choice(valid_moves)

                valid_positions = self.get_valid_moves_for_position(from_row, from_col)
                game_view.highlight_moves(valid_positions)

                pygame.display.flip()
                pygame.time.delay(1000)  # Delay for 1000 milliseconds (1 second)

                print(f"Computer moves from {from_row}, {from_col} to {to_row}, {to_col}")
                self.move_stack((from_row, from_col), (to_row, to_col))
            elif self.red_reserved > 0:  # If no valid moves but there are reserved pieces
                # select random move in board

                game_view.highlight_moves(
                    [(i, j) for i in range(self.board_size) for j in range(self.board_size) if
                     self.board[i][j] != 'N'])

                to_row, to_col = random.choice(
                    [(i, j) for i in range(self.board_size) for j in range(self.board_size) if self.board[i][j] != 'N'])
                self.move_reserved_piece(to_row, to_col, 'R')

        elif difficulty == 2:
            # Placeholder for Monte Carlo Tree Search
            pass
        elif difficulty == 3:
            # Placeholder for Minimax algorithm
            pass

        self.switch_turns()  # Switch turns at the end of the computer move
