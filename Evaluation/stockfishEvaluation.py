import chess
import chess.gaviota
import chess.engine
import chess.pgn
import chess.polyglot
import chess.svg
import chess.syzygy
import chess.variant



chess_engine = r"stockfish\stockfish-windows-x86-64-avx2.exe"


def stockfishEvaluation(board, agent):
    with chess.engine.SimpleEngine.popen_uci(chess_engine) as engine:
        info = engine.analyse(board, chess.engine.Limit(depth=1))

    score = info["score"].white() if agent else info["score"].black()

    if score.is_mate():
        mate_in = score.mate()
        return 100000 - abs(mate_in) * 1000 if mate_in > 0 else -100000 + abs(mate_in) * 1000
    else:
        return score.score() / 100.0
