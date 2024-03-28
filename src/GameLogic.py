import random

import pygame

from src.AI.MCTS import MCTS


class GameLogic:
    def __init__(self, board_size):
        self.board_size = board_size
        self.board = None
        self.initialize_board()
        self.turn = 'B'  # Blue player as default
        self.player = 'human' # Human player as default
        self.blue_reserved = 0
        self.red_reserved = 0
        self.blue_pieces = None
        self.red_pieces = None

    def initialize_board(self):
        if self.board_size == 8:

            # 8x8 board
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
                ['N', 'X', 'R', 'X', 'B', 'X', 'X', 'N'],
                ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
                ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
                ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
                ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
                ['N', 'X', 'X', 'X', 'X', 'X', 'X', 'N'],
                ['N', 'N', 'X', 'X', 'X', 'X', 'N', 'N']
            ]
        elif self.board_size == 6:

            # 6X6 board
            self.board = [
                ['N', 'N', 'X', 'X', 'N', 'N'],
                ['N', 'R', 'R', 'B', 'B', 'N'],
                ['X', 'B', 'B', 'R', 'R', 'X'],
                ['X', 'R', 'R', 'B', 'B', 'X'],
                ['N', 'B', 'B', 'R', 'R', 'N'],
                ['N', 'N', 'X', 'X', 'N', 'N']
            ]

        self.count_pieces()

    def copy(self):
        # Create a copy of the current game state
        new_board = GameLogic(self.board_size)
        new_board.board = [row.copy() for row in self.board]
        new_board.turn = self.turn
        new_board.blue_reserved = self.blue_reserved
        new_board.red_reserved = self.red_reserved
        new_board.blue_pieces = self.blue_pieces
        new_board.red_pieces = self.red_pieces
        return new_board

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

        num_pieces = len(stack)  # Number of pieces in the stack
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

        for dr, dc in directions:  # Check each direction
            for i in range(1, num_pieces + 1):
                new_row, new_col = row + dr * i, col + dc * i
                if 0 <= new_row < self.board_size and 0 <= new_col < self.board_size:  # Check if new position is
                    # within bounds
                    if self.board[new_row][new_col] == 'N':
                        break
                    valid_moves.append((new_row, new_col))  # Add the move if the space is either empty ('X'),
                    # contains opponent's piece on top, or contains player's own pieces
                else:
                    break

        return valid_moves

    def get_valid_moves_for_player(self, player):
        valid_moves = []
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board[row][col][-1] == player:  # Check if the top piece belongs to the player
                    piece_valid_moves = self.get_valid_moves_for_position(row, col)
                    for to_row, to_col in piece_valid_moves:  # Add the valid moves for the piece
                        valid_moves.append((row, col, to_row, to_col))  # Add the move to the list of valid moves
        return valid_moves

    def update_piece_counts(self, player, capture_count, reserve_count):
        if player == 'B':
            self.blue_reserved += reserve_count
            self.red_pieces -= capture_count
        else:
            self.red_reserved += reserve_count
            self.blue_pieces -= capture_count

    def calculate_distance(self, from_pos, to_pos):
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        return abs(to_row - from_row) + abs(to_col - from_col)

    def move_logic(self, from_pos, to_pos, player, moving_pieces, distance=None):
        to_row, to_col = to_pos

        if distance:
            moving_pieces = moving_pieces[-distance:] if len(moving_pieces) > distance else moving_pieces

        destination_stack = self.board[to_row][to_col] if self.board[to_row][to_col] != 'X' else ""
        final_stack = destination_stack + moving_pieces

        if len(final_stack) > 5:
            excess_pieces = final_stack[:len(final_stack) - 5]
            final_stack = final_stack[-5:]
        else:
            excess_pieces = ""

        capture_count = sum(1 for piece in excess_pieces if piece != player)
        reserve_count = len(excess_pieces) - capture_count

        if from_pos:
            from_row, from_col = from_pos
            self.board[from_row][from_col] = self.board[from_row][from_col][:-len(moving_pieces)] or 'X'

        self.board[to_row][to_col] = ''.join(final_stack) if final_stack else 'X'
        return capture_count, reserve_count

    def move_stack(self, from_pos, to_pos):
        from_row, from_col = from_pos
        moving_stack = self.board[from_row][from_col]
        player_moving = moving_stack[-1]

        distance = self.calculate_distance(from_pos, to_pos)  # Calculate the distance between the two positions

        capture_count, reserve_count = self.move_logic(from_pos, to_pos, player_moving, moving_stack, distance)
        self.update_piece_counts(player_moving, capture_count, reserve_count)

    def move_reserved_piece(self, to_pos, player):
        capture_count, reserve_count = self.move_logic(None, to_pos, player, player)
        self.update_piece_counts(player, capture_count, reserve_count - 1)  # Subtract one since we're using one reserve
        return True

    def check_winner(self):

        top_pieces = {'B': False, 'R': False}  # Track presence of top pieces for both players
        can_move = {'B': False, 'R': False}  # Track if the player can move any pieces

        for row in range(self.board_size):
            for col in range(self.board_size):
                stack = self.board[row][col]

                if stack in ['N', 'X'] or not stack:
                    continue

                top_piece = stack[-1]  # top-most piece of the stack
                top_pieces[top_piece] = True  # If the top piece is 'B', set top_pieces['B'] to True and vice versa

                # Check if there are valid moves for the piece at this position
                if self.get_valid_moves_for_position(row, col):
                    can_move[top_piece] = True

        has_reserved = {'B': self.blue_reserved > 0, 'R': self.red_reserved > 0}

        if top_pieces['B'] and not top_pieces['R']:  # If only blue pieces are on top and no red pieces
            return 'B' if not has_reserved['R'] and not can_move['R'] else None
        elif top_pieces['R'] and not top_pieces['B']:  # If only red pieces are on top and no blue pieces
            return 'R' if not has_reserved['B'] and not can_move['B'] else None
        else:
            if not can_move['B'] and not has_reserved['B'] and top_pieces['R'] and not top_pieces['B']:
                return 'R'
            elif not can_move['R'] and not has_reserved['R'] and top_pieces['B'] and not top_pieces['R']:
                return 'B'
            return None

    def switch_turns(self):
        self.turn = 'B' if self.turn == 'R' else 'R'  # Switch turns between Blue and Red
        self.player = 'human' if self.player == 'computer' else 'computer'  # Switch player between human and computer

    def highlight_and_move_computer(self, from_pos, to_pos, is_reserved, game_view):
        if is_reserved:
            game_view.highlight_moves(
                [(i, j) for i in range(self.board_size) for j in range(self.board_size) if self.board[i][j] != 'N'],
                reserved=True)
        else:
            valid_positions = self.get_valid_moves_for_position(from_pos[0], from_pos[1])
            game_view.highlight_moves(valid_positions, reserved=False)

        pygame.display.flip()
        pygame.time.delay(1000)

        if is_reserved:
            self.move_reserved_piece(to_pos, self.turn)  # Hardcoded for now (computer is always red)
        else:
            self.move_stack(from_pos, to_pos)

    def computer_move(self, mode, game_view, difficulty1, difficulty2):

        # if mode is 2 - only one computer player - only one difficulty
        # if mode is 3 - two computer players, difficulty might differ

        if mode == 2:
            difficulty = difficulty1
        elif mode == 3:
            if self.turn == 'B':  # First Player (Blue) has difficulty1
                difficulty = difficulty1
            else:
                difficulty = difficulty2  # Second Player (Red) has difficulty2
        else:
            difficulty = None

        if difficulty == 1:  # Easy - random

            print("Computer is moving - EASY")

            valid_moves = self.get_valid_moves_for_player(self.turn)

            if valid_moves:
                from_row, from_col, to_row, to_col = random.choice(valid_moves)
                self.highlight_and_move_computer((from_row, from_col), (to_row, to_col), is_reserved=False,
                                                 game_view=game_view)
            elif self.red_reserved > 0:
                to_row, to_col = random.choice(
                    [(i, j) for i in range(self.board_size) for j in range(self.board_size) if
                     self.board[i][j] != 'N'])
                self.highlight_and_move_computer(None, (to_row, to_col), is_reserved=True, game_view=game_view)
            else:
                print("No valid moves available")

        elif difficulty == 2:  # Medium - MCTS

            print("Computer is moving - MEDIUM")

            mcts_tree = MCTS(self, self.turn, 10)
            selected_move = mcts_tree.search()

            if selected_move:
                valid_positions = self.get_valid_moves_for_position(selected_move[0], selected_move[1])
                game_view.highlight_moves(valid_positions, reserved=False)
                pygame.display.flip()

                pygame.time.delay(1000)  # wait 1 second

                self.move_stack((selected_move[0], selected_move[1]), (selected_move[2], selected_move[3]))
            else:  # If no valid moves are available
                if self.red_reserved > 0:  # BUT there are reserved pieces

                    # Choose higher stack controlled by opponent
                    max_stack = 0
                    max_stack_pos = None
                    for i in range(self.board_size):
                        for j in range(self.board_size):
                            if self.board[i][j][-1] != self.turn and len(self.board[i][j]) > max_stack:
                                max_stack = len(self.board[i][j])
                                max_stack_pos = (i, j)

                    if max_stack_pos:
                        to_row, to_col = max_stack_pos

                        self.highlight_and_move_computer(None, (to_row, to_col), is_reserved=True, game_view=game_view)
                        pygame.display.flip()
                    else:
                        print("No valid moves available")

        elif difficulty == 3:
            # Placeholder for Minimax algorithm
            pass

    def check_gameover(self):
        return self.check_winner() is not None  # Game is over if there's a winner

    def get_result(self, player):
        winner = self.check_winner()  # Check the winner
        if winner == player:  # If the winner is the player
            return 1  # Win
        elif winner is None:
            return 0  # Game not done
        else:
            return -1  # Loss