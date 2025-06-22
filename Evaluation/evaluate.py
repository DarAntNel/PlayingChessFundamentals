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
        if piece and not piece.color:
            return False
    return True


def is_black_passer(board, square):
    file_idx = chess.square_file(square)
    for rank in range(8):
        check_square = chess.square(file_idx, rank)
        piece = board.piece_at(check_square)
        if piece and piece.color:
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

    b2 = board.copy(stack=False)
    b2.turn = is_white

    mobility = len([m for m in b2.legal_moves if m.from_square == square])
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


def evaluate_detailed_position(board,
                               agent: bool,
                               start_board,
                               captured,
                               moving_piece,
                               move_square):
    """
    board:        current position after the last move
    agent:        True for White-to-play evaluation, False for Black-to-play evaluation
    start_board:  board position before the last move
    captured:     symbol of the piece that was captured on the last move (or None)
    moving_piece: symbol of the piece that moved last
    move_square:  destination square index of the last move
    """
    our_color = chess.WHITE if agent else chess.BLACK

    # 1) start-state material & rank
    white_value_start = black_value_start = 0
    white_rank_start  = black_rank_start  = 0

    for sq in chess.SQUARES:
        p = start_board.piece_at(sq)
        if not p:
            continue
        s = p.symbol()
        if s in WHITE_PIECES:
            white_value_start += WHITE_PIECES[s]
            white_rank_start  += get_piece_rank(start_board, sq)
        elif s in BLACK_PIECES:
            black_value_start += BLACK_PIECES[s]
            black_rank_start  += get_piece_rank(start_board, sq)

    # 2) terminal checks
    if board.is_checkmate():
        return -10000 if board.turn == our_color else 10000
    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    # 3) threat matrix
    sol = [[] for _ in range(8)]
    row = col = 0

    for target in chess.SQUARES:
        w_atk = board.attackers(chess.WHITE, target)
        b_atk = board.attackers(chess.BLACK, target)
        victim = board.piece_at(target)

        w_cnt, b_cnt = len(w_atk), len(b_atk)
        w_val = sum(WHITE_PIECES.get(str(board.piece_at(s)), 0) for s in w_atk)
        b_val = sum(BLACK_PIECES.get(str(board.piece_at(s)), 0) for s in b_atk)

        w_score = b_score = 0

        # unified capture bonus
        if move_square == target and captured:
            if agent:  # White just moved
                w_score += (
                    WHITE_PIECES.get(moving_piece, 0) * 2
                    + BLACK_PIECES.get(captured, 0)
                    + chess.square_rank(target) + 1
                )
            else:      # Black just moved
                b_score += (
                    BLACK_PIECES.get(moving_piece, 0) * 2
                    + WHITE_PIECES.get(captured, 0)
                    + chess.square_rank(target) + 1
                )

        # pressure / counter-pressure
        if victim:
            sym = str(victim)

            if sym in BLACK_PIECES:
                # White pressuring Black
                if b_cnt and w_cnt:
                    if b_cnt == w_cnt:
                        b_score += b_cnt + w_val
                        w_score += BLACK_PIECES[sym] + b_val // (1 + b_cnt)
                    elif b_cnt > w_cnt:
                        b_score += b_cnt + w_val + 1
                        w_score += BLACK_PIECES[sym]
                elif b_cnt:
                    b_score += BLACK_PIECES[sym] + b_cnt
                elif w_cnt:
                    w_score += w_cnt + BLACK_PIECES[sym]
                else:
                    b_score += BLACK_PIECES[sym]

            elif sym in WHITE_PIECES:
                # Black pressuring White
                if b_cnt == w_cnt and w_cnt:
                    b_score += WHITE_PIECES[sym] + w_val // (1 + w_cnt)
                    w_score += b_val
                elif b_cnt == 0 and w_cnt == 0:
                    w_score += WHITE_PIECES[sym]
                elif w_cnt:
                    w_score += w_cnt + WHITE_PIECES[sym]
                elif b_cnt:
                    b_score += WHITE_PIECES[sym] + 1

                # victim’s own counter-attacks
                for s2 in board.attacks(target):
                    p2 = board.piece_at(s2)
                    if p2 and str(p2) in BLACK_PIECES:
                        b_score += BLACK_PIECES[str(p2)] + 1
                    else:
                        b_score += 1
        else:
            # empty square: simple attack pressure
            w_score += w_cnt
            b_score += b_cnt

        sol[row].append(w_score - b_score)
        col += 1
        if col == 8:
            col = 0
            row += 1

    # 4) end-state material & rank
    white_value_end = black_value_end = 0
    white_rank_end  = black_rank_end  = 0

    for sq in chess.SQUARES:
        p = board.piece_at(sq)
        if not p:
            continue
        s = p.symbol()
        if s in WHITE_PIECES:
            white_rank_end += get_piece_rank(board, sq)
            white_value_end += WHITE_PIECES[s]
        elif s in BLACK_PIECES:
            black_rank_end += get_piece_rank(board, sq)
            black_value_end += BLACK_PIECES[s]

    # 5) combine deltas
    white_delta = white_rank_end - white_rank_start
    black_delta = black_rank_end - black_rank_start

    white_loss = white_value_start - white_value_end
    black_loss = black_value_start - black_value_end

    white_final = white_delta - (white_loss ** 3) * 0.75
    black_final = black_delta + (black_loss ** 3) * 0.75

    # 6) sum threat + material/rank
    threat_sum = sum(sum(r) for r in sol)
    total = threat_sum + white_final + black_final

    # 7) return from agent’s POV
    return total if agent else -total


def evaluationFunction(board, agent, start_board=None, captured=None, moving_piece=None, move_square=None, use_detailed=False):
    if board.is_checkmate():
        return float('inf') if board.turn != agent else float('-inf')
    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    material_score = evaluate_material_and_position(board)
    threat_score = evaluate_attacks(board)
    mobility_score = 0.1 * board.legal_moves.count()

    detailed_score = 0
    if use_detailed:
        detailed_score = evaluate_detailed_position(
            board, agent, start_board=start_board, captured=captured, moving_piece=moving_piece, move_square=move_square)

    total_score = material_score + threat_score + mobility_score + detailed_score

    return total_score if agent == chess.WHITE else -total_score
