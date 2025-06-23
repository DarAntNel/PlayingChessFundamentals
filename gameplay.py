import asyncio
import copy
import logging
import os
import os.path
import platform
import sys
import tempfile
import textwrap
import time
import unittest
import io
import chess
import chess.gaviota
import chess.engine
import chess.pgn
import chess.polyglot
import chess.svg
import chess.syzygy
import chess.variant
import webbrowser
from Expectimax.expectimax import expectimax
from MiniMax.Minimax import minimax
from Alphabeta.alphabeta import alphabeta

from IPython.display import SVG, display
from LLM.groq_llm import get_move_from_groq

fen1 = "r1bqkb1r/ppp1pp1p/5np1/3p4/1P1P4/2NB1N2/P3PPPP/R1BQKB1R w KQkq - 0 61"
fen2 = "8/2b3p1/6P1/1kpPp3/1p1pB1b1/1P1P2B1/2PK4/8 w HAha - 0 1"
fen3 = "rnbqkbnr/pppp1ppp/4p3/6N1/8/8/PPPPPPPP/RNBQKB1R w KQkq - 0 1"

mates = [
    "6k1/8/5QK1/8/8/8/8/8 w - - 0 1",  # 0: King + Queen vs King (Mate in 1)
    "7k/4B3/6KN/8/8/8/8/8 w - - 0 1",  # 1: King +  Knight and Bishop   vs king (Mate in 1)
    "1k6/2R1N3/3K4/8/8/8/8/8 w - - 0 1",  # 3: King + knight and Rook vs King (Mate in 2)
    "1k6/8/2RKR3/8/8/8/8/8 w - - 0 1",  # 4: King + 2 Rook vs King (Mate in 2)
    "k7/1p6/1KP5/2N5/8/8/8/8 w - - 0 1"  # ,# 5 : Knight + Pawn (Mate in 2)
]

chess_engine = r"stockfish\stockfish-windows-x86-64-avx2.exe"

def getExpectimaxAction(board, depth, agent):
    bestScore = float('-inf')
    bestAction = ''
    legalMoves = list(board.legal_moves)
    print(legalMoves)
    if not legalMoves:
        return ''

    for move in legalMoves:
        prev = board.copy()
        mover = board.piece_at(move.from_square).symbol()
        cap = None
        if board.piece_at(move.to_square):
            cap = board.piece_at(move.to_square).symbol()
        to_sq = move.to_square

        board.push(move)
        score = expectimax(board, depth, agent,
                           start_board=prev,
                           captured=cap,
                           moving_piece=mover,
                           move_square=to_sq)
        board.pop()

        if score > bestScore:
            bestScore = score
            bestAction = move

    return bestAction

def getMinimaxAction(board, depth, agent):
    bestScore = float('-inf')
    bestAction = ''
    legalMoves = list(board.legal_moves)
    if not legalMoves:
        return ''

    for move in legalMoves:
        prev = board.copy()
        mover = board.piece_at(move.from_square).symbol()
        cap = None
        if board.piece_at(move.to_square):
            cap = board.piece_at(move.to_square).symbol()
        to_sq = move.to_square

        board.push(move)
        score = minimax(board, depth, agent,
                        start_board=prev,
                        captured=cap,
                        moving_piece=mover,
                        move_square=to_sq)
        board.pop()

        if score > bestScore:
            bestScore = score
            bestAction = move

    return bestAction


def getAlphabetaAction(board, depth, agent):
    bestScore = float('-inf')
    bestAction = None
    alpha = float('-inf')
    beta = float('inf')

    legalMoves = list(board.legal_moves)

    if not legalMoves:
        return None

    for move in legalMoves:
        successor = board.copy()
        successor.push(move)
        score = alphabeta(successor, depth -1, agent, alpha, beta)
        if score > bestScore:
            bestScore = score
            bestAction = move
        alpha = max(alpha, bestScore)
    return bestAction

def getStockFishAction(board):
    with chess.engine.SimpleEngine.popen_uci(chess_engine) as engine:
        engine.configure({"UCI_LimitStrength": True, "UCI_Elo": 1320})
        result = engine.play(board, chess.engine.Limit(time=0.1))
        return result.move



async def play_full_game_stockfish_vs_groc(board=chess.Board()):
    game = chess.pgn.Game()
    if board.fen() != chess.STARTING_FEN:
        game.setup(board)
    game.headers["Event"] = "stockfish_vs_groc"
    game.headers["White"] = "Groc"
    game.headers["Black"] = "Stockfish UCI_Elo 1320 "

    node = game
    pgn_path = "stockfish_vs_groc.pgn"
    while not board.is_game_over():
        move_str = await get_move_from_groq(board)
        print(move_str)
        print("LLM move:", move_str)

        try:
            move = board.parse_san(move_str)
            print(move)
            if move not in board.legal_moves:
                print("Illegal move:", move_str)
                break
        except Exception:
            print("Invalid SAN:", move_str)
            break

        board.push(move)
        node = node.add_variation(move)

        with open("test.svg", "w") as f:
            f.write(chess.svg.board(board))
        webbrowser.open('file://' + os.path.realpath("test.svg"))

        if board.is_game_over() or board.can_claim_threefold_repetition():
            break

        move_str = str(getStockFishAction(board))
        print(move_str)
        print("Stockfish move:", move_str)

        try:
            move = board.parse_san(move_str)
            print(move)
            if move not in board.legal_moves:
                print("Illegal move:", move_str)
                break
        except Exception:
            print("Invalid SAN:", move_str)
            break

        board.push(move)
        node = node.add_variation(move)

        with open("test.svg", "w") as f:
            f.write(chess.svg.board(board))
        webbrowser.open('file://' + os.path.realpath("test.svg"))

        if board.is_game_over() or board.can_claim_threefold_repetition():
            break

    result = board.result()
    print("Game over:", board.result())
    game.headers["Result"] = result
    with open(pgn_path, "a") as pgn_file:
        pgn_file.write(str(game) + "\n\n")
    print(f"Game saved to {pgn_path}")



async def play_full_game_expectimax_vs_stockfish(board=chess.Board(), depth=1):
    game = chess.pgn.Game()
    if board.fen() != chess.STARTING_FEN:
        game.setup(board)
    game.headers["Event"] = "expectimax_vs_stockfish"
    game.headers["White"] = "Stockfish UCI_Elo 1320"
    game.headers["Black"] = "Expectimax"
    node = game
    pgn_path = "expectimax_vs_stockfish.pgn"
    while not board.is_game_over():
        move_str = str(getStockFishAction(board))
        print(move_str)
        print("Stockfish move:", move_str)
        try:
            move = board.parse_san(move_str)
            print(move)
            if move not in board.legal_moves:
                print("Illegal move:", move_str)
                break
        except Exception:
            print("Invalid SAN:", move_str)
            break

        board.push(move)
        node = node.add_variation(move)

        with open("test.svg", "w") as f:
            f.write(chess.svg.board(board))
        webbrowser.open('file://' + os.path.realpath("test.svg"))

        if board.is_game_over() or board.can_claim_threefold_repetition():
            break

        move_str = str(getExpectimaxAction(board, depth, board.turn))
        print(move_str)
        print("Expectimax move:", move_str)

        try:
            move = board.parse_san(move_str)
            print(move)
            if move not in board.legal_moves:
                print("Illegal move:", move_str)
                break
        except Exception:
            print("Invalid SAN:", move_str)
            break

        board.push(move)
        node = node.add_variation(move)

        with open("test.svg", "w") as f:
            f.write(chess.svg.board(board))
        webbrowser.open('file://' + os.path.realpath("test.svg"))

        if board.is_game_over() or board.can_claim_threefold_repetition():
            break
    result = board.result()
    print("Game over:", board.result())
    game.headers["Result"] = result
    with open(pgn_path, "a") as pgn_file:
        pgn_file.write(str(game) + "\n\n")
    print(f"Game saved to {pgn_path}")

async def play_full_game_minimax_vs_stockfish(board=chess.Board(), depth=1):
    game = chess.pgn.Game()
    if board.fen() != chess.STARTING_FEN:
        game.setup(board)
    game.headers["Event"] = "minimax_vs_stockfish"
    game.headers["White"] = "Minimax"
    game.headers["Black"] = "Stockfish UCI_Elo 1320"
    node = game
    pgn_path = "minimax_vs_stockfish.pgn"

    while not board.is_game_over():
        move_str = str(getMinimaxAction(board, depth, board.turn))

        try:
            move = board.parse_san(move_str)
            print(move)
            if move not in board.legal_moves:
                print("Illegal move:", move_str)
                break
        except Exception:
            print("Invalid SAN:", move_str)
            break

        board.push(move)
        node = node.add_variation(move)

        with open("test.svg", "w") as f:
            f.write(chess.svg.board(board))
        webbrowser.open('file://' + os.path.realpath("test.svg"))

        if board.is_game_over() or board.can_claim_threefold_repetition():
            break

        move_str = str(getStockFishAction(board))
        print(move_str)
        print("Stockfish move:", move_str)

        try:
            move = board.parse_san(move_str)
            print(move)
            if move not in board.legal_moves:
                print("Illegal move:", move_str)
                break
        except Exception:
            print("Invalid SAN:", move_str)
            break

        board.push(move)
        node = node.add_variation(move)

        with open("test.svg", "w") as f:
            f.write(chess.svg.board(board))
        webbrowser.open('file://' + os.path.realpath("test.svg"))

        if board.is_game_over() or board.can_claim_threefold_repetition():
            break
    result = board.result()
    print("Game over:", board.result())
    game.headers["Result"] = result
    with open(pgn_path, "a") as pgn_file:
        pgn_file.write(str(game) + "\n\n")
    print(f"Game saved to {pgn_path}")




async def play_full_game_minimax_vs_expectimax(board=chess.Board(), depth=1):
    game = chess.pgn.Game()
    if board.fen() != chess.STARTING_FEN:
        game.setup(board)
    game.headers["Event"] = "minimax_vs_expectimax"
    game.headers["White"] = "Minimax"
    game.headers["Black"] = "Expectimax"
    node = game
    pgn_path = "minimax_vs_expectimax.pgn"

    while not board.is_game_over():
        move_str = str(getMinimaxAction(board, depth, board.turn))
        print(move_str)
        print("Minimax move:", move_str)
        try:
            move = board.parse_san(move_str)
            print(move)
            if move not in board.legal_moves:
                print("Illegal move:", move_str)
                break
        except Exception:
            print("Invalid SAN:", move_str)
            break

        board.push(move)
        node = node.add_variation(move)

        with open("test.svg", "w") as f:
            f.write(chess.svg.board(board))
        webbrowser.open('file://' + os.path.realpath("test.svg"))

        if board.can_claim_threefold_repetition():
            break

        move_str = str(getExpectimaxAction(board, depth, board.turn))
        print(move_str)
        print("Expectimax move:", move_str)

        try:
            move = board.parse_san(move_str)
            print(move)
            if move not in board.legal_moves:
                print("Illegal move:", move_str)
                break
        except Exception:
            print("Invalid SAN:", move_str)
            break

        board.push(move)
        node = node.add_variation(move)

        with open("test.svg", "w") as f:
            f.write(chess.svg.board(board))
        webbrowser.open('file://' + os.path.realpath("test.svg"))

        if board.is_game_over() or board.can_claim_threefold_repetition():
            break


    result = board.result()
    print("Game over:", board.result())
    game.headers["Result"] = result
    with open(pgn_path, "a") as pgn_file:
        pgn_file.write(str(game) + "\n\n")
    print(f"Game saved to {pgn_path}")





if __name__ == "__main__":

    asyncio.run(play_full_game_stockfish_vs_groc())

    for fen in mates:
        asyncio.run(play_full_game_minimax_vs_stockfish(chess.Board(fen)))
        asyncio.run(play_full_game_expectimax_vs_stockfish(chess.Board(fen)))


    count = 0
    while count < 4:
        asyncio.run(play_full_game_minimax_vs_stockfish())
        asyncio.run(play_full_game_minimax_vs_expectimax())
        asyncio.run(play_full_game_expectimax_vs_stockfish())
        count += 1








