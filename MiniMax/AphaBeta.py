
import chess
from EvaluatePositon import add_postionValue
#from startOverpy import  add_postionValue

positionValue=dict()
#with open("add_postionValueMay4th.pkl","rb") as f:
#    positionValue=pickle.load(f)


def findNextMove(board,startState, depth,captured,moving_piece,move_square):
         alpha=float("-inf")
         beta=float("inf")
         return maxValueAB(board,startState,depth,alpha,beta,captured,moving_piece,move_square)[1]
def maxValueAB(board,startState, depth, alpha, beta, captured, moving_piece, move_square):
    if depth == 0 or board.is_game_over():
        return add_postionValue(board,startState, captured, moving_piece, move_square), None

    bestMove = float('-inf')
    bestAction = None

    for action in board.legal_moves:
        captured_piece = board.piece_at(action.to_square)
        moving_piece = board.piece_at(action.from_square)

        board.push(action)
        value, _ = minValueAB(board,startState, depth - 1, alpha, beta, captured_piece, moving_piece, action.to_square)
        board.pop()

        if value > bestMove:
            bestMove = value
            bestAction = action

        alpha = max(alpha, bestMove)
        if beta <= alpha:
            break  # Alpha-beta pruning

    return bestMove, bestAction

def minValueAB(board,startState, depth, alpha, beta, captured, moving_piece, move_square):
    if depth == 0 or board.is_game_over():
        return add_postionValue(board,startState, captured, moving_piece, move_square), None

    worstMove = float('inf')
    worstAction = None

    for action in board.legal_moves:
        captured_piece = board.piece_at(action.to_square)
        moving_piece = board.piece_at(action.from_square)

        board.push(action)
        #print(board.peek())
        CostToMove, _ = maxValueAB(board,startState, depth - 1, alpha, beta, captured_piece, moving_piece, action.to_square)
        board.pop()


        if CostToMove < worstMove:
            worstMove = CostToMove
            worstAction = action

        beta = min(beta, worstMove)
        if beta <= alpha:
            break  # Alpha-beta pruning
    return worstMove, worstAction
