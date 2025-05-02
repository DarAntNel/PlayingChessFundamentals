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
from IPython.display import SVG, display
import webbrowser

def evaluationFunction(board):
    return board.legal_moves.count()



def expectimax(board, depth, agent):
    if depth == 0 or board.is_game_over() or board.is_checkmate():
        return evaluationFunction(board)

    if board.turn == chess.WHITE:
        nextAgent = chess.BLACK
    else:
        nextAgent = chess.WHITE

    nextDepth = depth - 1 if board.turn == chess.WHITE else depth

    legalMoves = board.legal_moves

    if not legalMoves:
        return evaluationFunction(board)

    if board.turn == chess.WHITE:
        maxEval = float('-inf')
        for move in legalMoves:
            sucessor = chess.Board(board.fen())
            sucessor.push_san(str(move))
            # with open("test.svg", "w") as f:
            #     f.write(chess.svg.board(sucessor))
            # webbrowser.open('file://' + os.path.realpath("test.svg"))
            evalScore = expectimax(sucessor, nextDepth, nextAgent)
            maxEval = max(maxEval, evalScore)
        return maxEval
    else:
        total = 0
        probability = 1 / legalMoves.count()
        for move in legalMoves:
            sucessor = chess.Board(board.fen())
            sucessor.push_san(str(move))
            # with open("test.svg", "w") as f:
            #     f.write(chess.svg.board(sucessor))
            # webbrowser.open('file://' + os.path.realpath("test.svg"))
            evalScore = expectimax(sucessor, nextDepth, nextAgent)
            total += probability * evalScore
        return total


def getAction(board, depth):
    bestScore = float('-inf')
    bestAction = None
    legalMoves = board.legal_moves

    for move in legalMoves:
        sucessor = chess.Board(board.fen())
        sucessor.push_san(str(move))
        score = expectimax(sucessor, depth, sucessor.turn)
        if score > bestScore:
            bestScore = score
            bestAction = move
    return bestAction

board = chess.Board()
depth=int(sys.argv[1])

with open("test.svg", "w") as f:
    f.write(chess.svg.board(board))
webbrowser.open('file://' + os.path.realpath("test.svg"))

count = 0

while count < 100:
    action = getAction(board, depth)
    board.push_san(str(action))

    with open("test.svg", "w") as f:
        f.write(chess.svg.board(board))
    webbrowser.open('file://' + os.path.realpath("test.svg"))

    count += 1

