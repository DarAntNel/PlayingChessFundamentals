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

from Evaluation import evaluate
from IPython.display import SVG, display

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




def getAction(board, depth):
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



board = chess.Board(mates[2])
depth=int(sys.argv[1])

with open("test.svg", "w") as f:
    f.write(chess.svg.board(board))
webbrowser.open('file://' + os.path.realpath("test.svg"))

count = 0

while count < 100:
    action = getAction(board, depth)
    if not action and board.is_game_over():
            print("Game over.")
            outcome = board.outcome()
            if outcome:
                if outcome.winner == chess.WHITE:
                    print("White wins!")
                elif outcome.winner == chess.BLACK:
                    print("Black wins!")
                else:
                    print("The game is a draw.")
            break
    else:
        board.push_san(str(action))
    time.sleep(1)

    with open("test.svg", "w") as f:
        f.write(chess.svg.board(board))
    webbrowser.open('file://' + os.path.realpath("test.svg"))

    count += 1





