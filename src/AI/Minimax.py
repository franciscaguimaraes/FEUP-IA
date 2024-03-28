class Minimax:
    def __init__(self, depth, player):
        self.depth = depth
        self.player = player  # 'B' or 'R'

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

    def minimax(self, game_logic, depth, maximizingPlayer):
        if depth == 0 or game_logic.check_gameover():
            return self.evaluate(game_logic)

        if maximizingPlayer:
            maxEval = float('-inf')
            for move in game_logic.get_valid_moves_for_player(self.player):
                new_game_state = game_logic.copy()
                new_game_state.move_stack(move[:2], move[2:])
                eval = self.minimax(new_game_state, depth - 1, False)
                maxEval = max(maxEval, eval)
            return maxEval
        else:
            minEval = float('inf')
            opponent = 'B' if self.player == 'R' else 'R'
            for move in game_logic.get_valid_moves_for_player(opponent):
                new_game_state = game_logic.copy()
                new_game_state.move_stack(move[:2], move[2:])
                eval = self.minimax(new_game_state, depth - 1, True)
                minEval = min(minEval, eval)
            return minEval

    def find_best_move(self, game_logic):
        best_move = None
        best_score = float('-inf') if self.player == game_logic.turn else float('inf')

        for move in game_logic.get_valid_moves_for_player(self.player):
            new_game_state = game_logic.copy()
            new_game_state.move_stack(move[:2], move[2:])
            score = self.minimax(new_game_state, self.depth - 1, game_logic.turn != self.player)

            if self.player == game_logic.turn and score > best_score:
                best_score = score
                best_move = move
            elif self.player != game_logic.turn and score < best_score:
                best_score = score
                best_move = move

        return best_move
