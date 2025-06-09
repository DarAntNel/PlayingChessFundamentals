def evaluationFunction(board, agent):
    if board.is_checkmate():
        return float('-inf')

    number_piece_value = {i: 64 - 4 * i for i in range(17)}

    score = 0
    positions = set()
    named_positions = []
    op_type_count = {}
    total_op_type_count = 0


    for piece_type in chess.PIECE_TYPES:
        positions.update(board.pieces(piece_type, agent))
    for position in positions:
        named_positions.append(chess.SQUARE_NAMES[position])


    if agent == chess.WHITE:
        for piece_type in chess.PIECE_TYPES:
            op_type_count[piece_type] = len(board.pieces(piece_type, chess.BLACK))
            total_op_type_count += len(board.pieces(piece_type, chess.BLACK))
    else:
        for piece_type in chess.PIECE_TYPES:
            op_type_count[piece_type] = len(board.pieces(piece_type, chess.WHITE))
            total_op_type_count += len(board.pieces(piece_type, chess.WHITE))

    # with open("test.svg", "w") as f:
    #     f.write(chess.svg.board(board))
    # webbrowser.open('file://' + os.path.realpath("test.svg"))

    for square in positions:
        if board.is_attacked_by(chess.BLACK, square):
            score += 2
        if board.attackers(chess.BLACK, square):
            score -= 3


    score += board.legal_moves.count() + number_piece_value[total_op_type_count]


    return score

