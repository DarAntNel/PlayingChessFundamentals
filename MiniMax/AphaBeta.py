
import chess
from EvaluatePositon import add_postionValue
#from startOverpy import  add_postionValue

positionValue=dict()
#with open("add_postionValueMay4th.pkl","rb") as f:
#    positionValue=pickle.load(f)


def findNextMove(board,startState, depth,captured,moving_piece,move_square):
         return maxValueAB(board,startState, depth,captured,moving_piece,move_square)[1]

def maxValueAB(board,startState, depth,captured,moving_piece,move_square):

    if  depth==0 or  board.is_game_over():
        #print("turn=White",board.turn==chess.WHITE)
        return  add_postionValue(board,startState, depth,captured,moving_piece,move_square),None

    bestMove=float('-inf')
    bestAction=None

    for actions in board.legal_moves:
        captured = board.piece_at(actions.to_square)
        moving_piece=board.piece_at(actions.from_square)
        board.push(actions)
        CostToMove=minValue(board,startState, depth-1,captured,moving_piece,actions.to_square)[0]
        board.pop()
        if CostToMove>bestMove:
           bestMove=CostToMove
           bestAction=actions

    return bestMove,bestAction
    #simulating black is move
def minValue(board,startState, depth,captured,moving_piece,move_square):
    if  depth ==0 or board.is_game_over():
        return  add_postionValue(board,startState, depth,captured,moving_piece,move_square),None
    worstMove=float('inf')
    worstAction=None

    for actions in board.legal_moves:
        captured = board.piece_at(actions.to_square)
        moving_piece=board.piece_at(actions.from_square)
        board.push(actions)
        costToMove=maxValueAB(board,board,startState, depth-1,captured,moving_piece,actions.to_square)[0]
        board.pop()
        if worstMove>costToMove:
            worstMove=costToMove
            worstAction=actions

    return worstMove,worstAction
