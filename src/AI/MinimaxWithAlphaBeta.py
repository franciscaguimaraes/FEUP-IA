class MinimaxWithAlphaBeta:
    def __init__(self, depth, player, game_level):
        self.depth = depth
        self.player = player  # 'B' ou 'R'
        self.game_level = game_level # 2 or 3 or 4

    def evaluate_2(self, game_logic):
        score = 0
        for row in game_logic.board:
            for cell in row:
                if cell not in ['N', 'X', '']:
                    stack_owner = cell[-1]
                    stack_points = len(cell)
                    if stack_owner == self.player:
                        score += stack_points
                    else:
                        score -= stack_points
        score += game_logic.blue_reserved if self.player == 'B' else game_logic.red_reserved
        score += game_logic.red_captured if self.player == 'B' else game_logic.blue_captured
        return score

    def evaluate_3(self, game_logic, move):
        if move is None:
            return 0
        score = 0
        source, destination = move[:2], move[2:]

        # Check for opponent pieces in all 4 directions
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
        for dx, dy in directions:
            x, y = destination
            adj_x, adj_y = x + dx, y + dy
            if 0 <= adj_x < len(game_logic.board) and 0 <= adj_y < len(game_logic.board[0]):
                adj_cell = game_logic.board[adj_x][adj_y]
                if adj_cell and adj_cell[-1] != self.player and adj_cell[-1] not in ['N', 'X', '']:
                    # Found opponent piece in this direction, increment score
                    score += 1
        # If piece has opponent's pieces in all 4 directions, increase its value
        if score == 4:
            score += 10  # Arbitrary value to signify the importance

        # Check for placing in a stack of 5 that ends with player's piece
        dest_cell = game_logic.board[destination[0]][destination[1]]
        if len(dest_cell) == 4 and dest_cell[-1] == self.player:
            score += 5  # Again, an arbitrary value to indicate importance

        return score

    def minimax(self, game_logic, depth, alpha, beta, maximizingPlayer,  move=None):
        if depth == 0 or game_logic.check_gameover():
            if self.game_level == 3 or self.game_level == 4:
                eval = self.evaluate_2(game_logic)
            elif self.game_level == 2:
                eval = self.evaluate_3(game_logic, move)
            else:
                eval = 0
            print(f"{' ' * (4 - depth)}Eval: {eval}, Depth: {depth}, Alpha: {alpha}, Beta: {beta}")
            return eval

        if maximizingPlayer:
            maxEval = float('-inf')
            print(f"{' ' * (4 - depth)}Maximizing, Depth: {depth}, Alpha: {alpha}, Beta: {beta}")
            for move in game_logic.get_valid_moves_for_player(self.player):
                new_game_state = game_logic.copy()
                new_game_state.move_stack(move[:2], move[2:])
                eval = self.minimax(new_game_state, depth - 1, alpha, beta, False, move)
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    print(f"{' ' * (4 - depth)}Alpha cut-off at {alpha}")
                    break
            return maxEval
        else:
            minEval = float('inf')
            print(f"{' ' * (4 - depth)}Minimizing, Depth: {depth}, Alpha: {alpha}, Beta: {beta}")
            opponent = 'B' if self.player == 'R' else 'R'
            for move in game_logic.get_valid_moves_for_player(opponent):
                new_game_state = game_logic.copy()
                new_game_state.move_stack(move[:2], move[2:])
                eval = self.minimax(new_game_state, depth - 1, alpha, beta, True, move)
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    print(f"{' ' * (4 - depth)}Beta cut-off at {beta}")
                    break
            return minEval

    def find_best_move(self, game_logic):
        best_move = None
        best_score = float('-inf') if self.player == game_logic.turn else float('inf')
        alpha = float('-inf')
        beta = float('inf')

        print(f"{'=' * 20}\nStarting Minimax Search for Player {self.player}")
        for move in game_logic.get_valid_moves_for_player(self.player):
            new_game_state = game_logic.copy()
            new_game_state.move_stack(move[:2], move[2:])
            # Chama minimax com o movimento atual
            score = self.minimax(new_game_state, self.depth - 1, alpha, beta, game_logic.turn != self.player, move)
            # Lógica para atualizar o melhor movimento baseado no score
            if (self.player == game_logic.turn and score > best_score) or (
                    self.player != game_logic.turn and score < best_score):
                best_score = score
                best_move = move
                if self.player == game_logic.turn:
                    alpha = max(alpha, score)
                else:
                    beta = min(beta, score)
            print(f"Considered Move: {move}, Score: {score}, Alpha: {alpha}, Beta: {beta}")

        print(f"Best Move: {best_move}, Best Score: {best_score}")
        return best_move
