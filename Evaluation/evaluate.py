import chess

import chess
import numpy as np

# Piece values
PIECE_VALUES = {'p': 1, 'n': 3, 'b': 3, 'r': 5, 'q': 9, 'k': 0,
                'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 0}
WHITE_PIECES = {k: v for k, v in PIECE_VALUES.items() if k.isupper()}
BLACK_PIECES = {k: v for k, v in PIECE_VALUES.items() if k.islower()}


def is_white_passer(board, square):
    file_idx = chess.square_file(square)
    for rank in range(8):
        check_square = chess.square(file_idx, rank)
        piece = board.piece_at(check_square)
        if piece and not piece.color:  # If black piece exists
            return False
    return True


def is_black_passer(board, square):
    file_idx = chess.square_file(square)
    for rank in range(8):
        check_square = chess.square(file_idx, rank)
        piece = board.piece_at(check_square)
        if piece and piece.color:  # If white piece exists
            return False
    return True


def get_piece_rank(board, square):
    piece = board.piece_at(square)
    if not piece:
        return 0

    is_white = piece.color
    piece_type = piece.symbol()

    if piece_type in ('P', 'p'):
        rank = chess.square_rank(square) + 1 if is_white else 8 - chess.square_rank(square)
        if (is_white and is_white_passer(board, square)) or (not is_white and is_black_passer(board, square)):
            return rank ** 2
        return rank

    if piece_type in ('K', 'k'):
        return 0

    board.turn = is_white
    mobility = len([m for m in board.legal_moves if m.from_square == square])
    return mobility


def evaluate_material_and_position(board):
    score = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if not piece:
            continue
        piece_symbol = piece.symbol()
        value = PIECE_VALUES[piece_symbol]
        rank_bonus = get_piece_rank(board, square)

        if piece.color == chess.WHITE:
            score += value + 0.1 * rank_bonus
        else:
            score -= value + 0.1 * rank_bonus
    return score


def evaluate_attacks(board):
    score = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if not piece:
            continue

        attackers_white = board.attackers(chess.WHITE, square)
        attackers_black = board.attackers(chess.BLACK, square)

        if piece.color == chess.WHITE:
            score -= len(attackers_black)
        else:
            score += len(attackers_white)
    return score


def evaluationFunction(board, agent):
    if board.is_checkmate():
        return float('inf') if board.turn != agent else float('-inf')
    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    material_score = evaluate_material_and_position(board)
    threat_score = evaluate_attacks(board)
    mobility_score = 0.1 * board.legal_moves.count()

    total_score = material_score + threat_score + mobility_score

    return total_score if agent == chess.WHITE else -total_score
