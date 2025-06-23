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




def expectimax(board, depth, agent,
               start_board=None, captured=None, moving_piece=None, move_square=None):

    if depth == 0 or board.is_game_over() or board.is_checkmate():
        return evaluationFunction(
            board, agent,
            start_board=start_board,
            captured=captured,
            moving_piece=moving_piece,
            move_square=move_square,
            use_detailed=True
        )

    # Whose turn next?
    if board.turn == chess.WHITE:
        nextAgent = chess.BLACK
    else:
        nextAgent = chess.WHITE

    # Always consume one ply
    nextDepth = depth - 1

    legalMoves = list(board.legal_moves)
    if not legalMoves:
        return evaluationFunction(
            board, agent,
            start_board=start_board,
            captured=captured,
            moving_piece=moving_piece,
            move_square=move_square,
            use_detailed=True
        )

    if board.turn == agent:
        maxEval = float('-inf')
        for move in legalMoves:
            prev = board.copy()
            mover = board.piece_at(move.from_square).symbol()
            cap = None
            if board.piece_at(move.to_square):
                cap = board.piece_at(move.to_square).symbol()
            to_sq = move.to_square

            board.push(move)
            val = expectimax(board, nextDepth, agent,
                             start_board=prev,
                             captured=cap,
                             moving_piece=mover,
                             move_square=to_sq)
            board.pop()

            maxEval = max(maxEval, val)
        return maxEval
    else:
        total = 0.0
        for move in legalMoves:
            prev = board.copy()
            mover = board.piece_at(move.from_square).symbol()
            cap = None
            if board.piece_at(move.to_square):
                cap = board.piece_at(move.to_square).symbol()
            to_sq = move.to_square

            board.push(move)
            val = expectimax(board, depth, agent,
                             start_board=prev,
                             captured=cap,
                             moving_piece=mover,
                             move_square=to_sq)
            board.pop()

            total += val
        return total / len(legalMoves)





