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
    "6k1/5Q2/8/8/8/8/8/6K1 w - - 0 1",
    "6k1/8/8/8/8/8/5Q2/6K1 w - - 0 1",  # 0: King + Queen vs King (Mate in 1)
    "6k1/8/8/8/8/8/5R2/6K1 w - - 0 1",  # 1: King + Rook vs King (Mate in 1)
    "6k1/6P1/8/8/6B1/8/8/6K1 w - - 0 1",  # 2: King + Bishop + Pawn (Mate in 1)
    "6k1/8/8/8/8/5Q2/8/6K1 w - - 0 1",  # 3: King + Queen vs King (Mate in 2)
    "6k1/8/8/8/8/5R2/8/6K1 w - - 0 1",  # 4: King + Rook vs King (Mate in 2)
    "6k1/5P2/7K/8/8/5n2/8/8 w - - 0 1",  # 5: Knight + Pawn (Mate in 2)
    "6k1/8/8/8/8/4Q3/8/6K1 w - - 0 1",  # 6: King + Queen vs King (Mate in 3)
    "7k/8/8/8/8/8/5R2/6K1 w - - 0 1",  # 7: King + Rook vs King (Mate in 3)
    "6k1/8/8/3B4/8/8/6K1/8 w - - 0 1",  # 8: Bishop Mate (Mate in 3)
]

chess_engine = r"stockfish\stockfish-windows-x86-64-avx2.exe"

def getExpectimaxAction(board, depth):
    bestScore = float('-inf')
    bestAction = ''
    legalMoves = board.legal_moves

    if not legalMoves:
        return ''
    for move in legalMoves:
        sucessor = chess.Board(board.fen())
        sucessor.push_san(str(move))
        score = expectimax(sucessor, depth, sucessor.turn)
        if score > bestScore:
            bestScore = score
            bestAction = move
    return bestAction

def getMinimaxAction(board, depth):
    bestScore = float('-inf')
    bestAction = ''
    legalMoves = list(board.legal_moves)

    if not legalMoves:
        return ''

    for move in legalMoves:
        successor = chess.Board(board.fen())
        successor.push_san(str(move))
        score = minimax(successor, depth, successor.turn)
        if score > bestScore:
            bestScore = score
            bestAction = move
    return bestAction


def getAlphabetaAction(board, depth):
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
        score = alphabeta(successor, depth, successor.turn, alpha, beta)
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



async def play_full_game_llm_vs_groc(board=chess.Board()):

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

        with open("test.svg", "w") as f:
            f.write(chess.svg.board(board))
        webbrowser.open('file://' + os.path.realpath("test.svg"))

        if board.can_claim_threefold_repetition():
            print("Threefold repetition detected! Game can be ended as a draw.")
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

        with open("test.svg", "w") as f:
            f.write(chess.svg.board(board))
        webbrowser.open('file://' + os.path.realpath("test.svg"))

        if board.can_claim_threefold_repetition():
            print("Threefold repetition detected! Game can be ended as a draw.")
            break

    print("Game over:", board.result())



async def play_full_game_expectimax_vs_stockfish(board=chess.Board(), depth = 1):

    while not board.is_game_over():
        move_str = str(getExpectimaxAction(board, depth))

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

        with open("test.svg", "w") as f:
            f.write(chess.svg.board(board))
        webbrowser.open('file://' + os.path.realpath("test.svg"))

        if board.can_claim_threefold_repetition():
            print("Threefold repetition detected! Game can be ended as a draw.")
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

        with open("test.svg", "w") as f:
            f.write(chess.svg.board(board))
        webbrowser.open('file://' + os.path.realpath("test.svg"))

        if board.can_claim_threefold_repetition():
            print("Threefold repetition detected! Game can be ended as a draw.")
            break
    if(board.is_checkmate()):
        rint("Check Mate:")
    print("Game over:", board.result())

async def play_full_game_minimax_vs_stockfish(board=chess.Board(), depth=1):

    while not board.is_game_over():
        move_str = str(getMinimaxAction(board, depth))

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

        with open("test.svg", "w") as f:
            f.write(chess.svg.board(board))
        webbrowser.open('file://' + os.path.realpath("test.svg"))

        if board.can_claim_threefold_repetition():
            print("Threefold repetition detected! Game can be ended as a draw.")
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

        with open("test.svg", "w") as f:
            f.write(chess.svg.board(board))
        webbrowser.open('file://' + os.path.realpath("test.svg"))

        if board.can_claim_threefold_repetition():
            print("Threefold repetition detected! Game can be ended as a draw.")
            break
    if (board.is_checkmate()):
        rint("Check Mate:")
    print("Game over:", board.result())










if __name__ == "__main__":

    # depth = int(sys.argv[1])
    asyncio.run(play_full_game_minimax_vs_stockfish())


    # if sys.argv[2] and int(sys.argv[2]) == 1:
    #     board = chess.Board(mates[2])
    #     asyncio.run(play_full_game(board))
    # else:
    # asyncio.run(play_full_game())



