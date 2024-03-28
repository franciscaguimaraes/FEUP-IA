
import pygame

class Minimax:

    def minimaxAlphaBeta(board, color, depth, alpha, beta, evaluate, maximizing_player):
        if depth == 0 or board.check_gameover(color):
            # prioritize the move which makes the player win
            if board.check_gameover(color):
                return 99999999
            return evaluate(board)

        if maximizing_player:
            max_flag = 0
            max_eval = float('-inf')
            for piece in board.get_pieces():
                for move in piece.occupying_piece.get_moves(board):
                    new_board = piece.occupying_piece.experimental_move(board, move)
                    eval = minimaxAlphaBeta(new_board, color, depth - 1, alpha, beta, evaluate, False)
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        max_flag = 1
                        break
                if max_flag:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            min_flag = 0
            for piece in board.get_pieces():
                for move in piece.occupying_piece.get_moves(board):
                    new_board = piece.occupying_piece.experimental_move(board, move)
                    eval = minimaxAlphaBeta(new_board, color, depth - 1, alpha, beta, evaluate, True)
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        min_flag = 1
                        break
                if min_flag:
                    break
            return min_eval
