class MinimaxWithAlphaBeta:
    def __init__(self, depth, player):
        self.depth = depth
        self.player = player  # 'B' ou 'R'

    def evaluate(self, game_logic):
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
        return score

    def minimax(self, game_logic, depth, alpha, beta, maximizingPlayer):
        if depth == 0 or game_logic.check_gameover():
            eval = self.evaluate(game_logic)
            print(f"{' ' * (4 - depth)}Eval: {eval}, Depth: {depth}, Alpha: {alpha}, Beta: {beta}")
            return eval

        if maximizingPlayer:
            maxEval = float('-inf')
            print(f"{' ' * (4 - depth)}Maximizing, Depth: {depth}, Alpha: {alpha}, Beta: {beta}")
            for move in game_logic.get_valid_moves_for_player(self.player):
                new_game_state = game_logic.copy()
                new_game_state.move_stack(move[:2], move[2:])
                eval = self.minimax(new_game_state, depth - 1, alpha, beta, False)
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
                eval = self.minimax(new_game_state, depth - 1, alpha, beta, True)
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

        print(f"{'='*20}\nStarting Minimax Search for Player {self.player}")
        for move in game_logic.get_valid_moves_for_player(self.player):
            new_game_state = game_logic.copy()
            new_game_state.move_stack(move[:2], move[2:])
            score = self.minimax(new_game_state, self.depth - 1, alpha, beta, game_logic.turn != self.player)
            if self.player == game_logic.turn and score > best_score:
                best_score = score
                best_move = move
                alpha = max(alpha, score)
            elif self.player != game_logic.turn and score < best_score:
                best_score = score
                best_move = move
                beta = min(beta, score)
            print(f"Considered Move: {move}, Score: {score}, Alpha: {alpha}, Beta: {beta}")

        print(f"Best Move: {best_move}, Best Score: {best_score}")
        return best_move
