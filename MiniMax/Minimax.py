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
from Evaluation.stockfishEvaluation import stockfishEvaluation
from IPython.display import SVG, display
from Evaluation.evaluate import evaluationFunction

def minimax(board, depth, agent):
    if depth == 0 or board.is_game_over() or board.is_checkmate():
        return evaluationFunction(board, agent)

    if board.turn == chess.WHITE:
        nextAgent = chess.BLACK
    else:
        nextAgent = chess.WHITE

    nextDepth = depth - 1 if board.turn == chess.WHITE else depth

    legalMoves = list(board.legal_moves)

    if not legalMoves:
        return evaluationFunction(board, agent)

    if board.turn == chess.WHITE:
        maxEval = float('-inf')
        for move in legalMoves:
            successor = chess.Board(board.fen())
            successor.push_san(str(move))
            evalScore = minimax(successor, nextDepth, nextAgent)
            maxEval = max(maxEval, evalScore)
        return maxEval
    else:
        minEval = float('inf')
        for move in legalMoves:
            successor = chess.Board(board.fen())
            successor.push_san(str(move))
            evalScore = minimax(successor, nextDepth, nextAgent)
            minEval = min(minEval, evalScore)
        return minEval
