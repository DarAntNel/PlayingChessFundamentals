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
from Evaluation.evaluate import evaluationFunction
from IPython.display import SVG, display




def expectimax(board, depth, agent):
    if depth == 0 or board.is_game_over() or board.is_checkmate():
        return evaluationFunction(board, agent)

    if board.turn == chess.WHITE:
        nextAgent = chess.BLACK
    else:
        nextAgent = chess.WHITE

    nextDepth = depth - 1 if board.turn == chess.WHITE else depth

    legalMoves = board.legal_moves

    if not legalMoves:
        return evaluationFunction(board, agent)

    if board.turn == chess.WHITE:
        maxEval = float('-inf')
        for move in legalMoves:
            sucessor = chess.Board(board.fen())
            sucessor.push_san(str(move))
            evalScore = expectimax(sucessor, nextDepth, nextAgent)
            maxEval = max(maxEval, evalScore)
        return maxEval
    else:
        total = 0
        probability = 1 / legalMoves.count()
        for move in legalMoves:
            sucessor = chess.Board(board.fen())
            sucessor.push_san(str(move))
            evalScore = expectimax(sucessor, nextDepth, nextAgent)
            total += probability * evalScore
        return total





