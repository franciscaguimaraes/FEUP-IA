import math
import random

class MCTSNode:
    def __init__(self, game_state, turn, move=None, parent=None):
        self.game_state = game_state.copy()
        self.move = move
        self.turn = turn
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0

    def expand(self):
        for move_info in self.game_state.get_valid_moves_for_player(self.turn):
            from_row, from_col, to_row, to_col = move_info
            new_game_state = self.game_state.copy()
            new_game_state.move_stack((from_row, from_col), (to_row, to_col))
            new_game_state.switch_turns()

            child = MCTSNode(new_game_state, new_game_state.turn, move=move_info, parent=self)
            self.children.append(child)

    def select(self):
        c = 1.4
        total_visits = sum(child.visits for child in self.children)
        log_total_visits = math.log(total_visits) if total_visits > 0 else 1

        best_score = float('-inf')
        best_child = None

        for child in self.children:
            if child.visits == 0:
                score = float('inf')
            else:
                exploitation = child.wins / child.visits
                exploration = c * math.sqrt(log_total_visits / child.visits)
                score = exploitation + exploration

            if score > best_score:
                best_score = score
                best_child = child

        # object best_child keeps turn B, but the game state is R to obey algorithm search
        best_child.game_state.switch_turns()

        return best_child

    def simulate(self):
        current_state = self.game_state.copy()

        while not current_state.check_gameover():
            valid_moves = current_state.get_valid_moves_for_player(current_state.turn)
            if not valid_moves:
                break
            move = random.choice(valid_moves)
            from_row, from_col, to_row, to_col = move

            current_state.move_stack((from_row, from_col), (to_row, to_col))
            current_state.switch_turns()

        return current_state.get_result(current_state.turn)

    def backpropagate(self, result):
        self.visits += 1
        self.wins += result
        if self.parent:
            self.parent.backpropagate(result)


class MCTS:
    def __init__(self, game_state, turn, max_iterations):
        self.root = MCTSNode(game_state, turn)
        self.max_iterations = max_iterations

    def search(self):
        for _ in range(self.max_iterations):
            node = self.root

            if not node.children and node.visits == 0:
                node.expand()

            while node.children:
                node = node.select()
            result = node.simulate()

            node.backpropagate(result)

        if not self.root.children:  # If there are no children
            return None
        else:
            most_wins = max(self.root.children, key=lambda child: child.wins).wins
            best_children = [child for child in self.root.children if child.wins == most_wins]
            best_child = random.choice(best_children)

            return best_child.move