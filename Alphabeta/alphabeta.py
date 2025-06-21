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


def alphabeta(board, depth, agent, alpha=float('-inf'), beta=float('inf')):
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
            successor = board.copy()
            successor.push(move)
            evalScore = minimax(successor, nextDepth, nextAgent, alpha, beta)
            maxEval = max(maxEval, evalScore)
            alpha = max(alpha, evalScore)
            if beta <= alpha:
                break  # Beta cut-off
        return maxEval
    else:
        minEval = float('inf')
        for move in legalMoves:
            successor = board.copy()
            successor.push(move)
            evalScore = minimax(successor, nextDepth, nextAgent, alpha, beta)
            minEval = min(minEval, evalScore)
            beta = min(beta, evalScore)
            if beta <= alpha:
                break  # Alpha cut-off
        return minEval
