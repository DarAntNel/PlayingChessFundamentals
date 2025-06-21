
import chess
from concurrent.futures import ProcessPoolExecutor
import copy
import os
#import movesDict
#from EvalSnapshot import  add_postionValue
#from EvaluatePositon import add_postionValue
from EvaluatePositonModified import add_postionValue

#from NewIdeamay20_1109 import add_postionValue
#from Snpshot28_955 import add_postionValue # whins playmates easilly'''


positionValue=dict()
#with open("add_postionValueMay4th.pkl","rb") as f:
#    positionValue=pickle.load(f)


def findNextMove(board,startState, depth,captured,moving_piece,move_square,single=False):
         if single==True:
             #return maxValue(board,startState, depth,captured,moving_piece,move_square)[1]
             return parallelMax(board,startState, depth,captured,moving_piece,move_square)[1]
         else:
             return maxValue(board,startState, depth,captured,moving_piece,move_square)[1]
def evaluate_move_root(args):
    board, startState, depth, move = args
    board = copy.deepcopy(board)
    captured = board.piece_at(move.to_square)
    moving_piece = board.piece_at(move.from_square)
    board.push(move)
    cost = minValue(board, startState, depth - 1, captured, moving_piece, move.to_square)[0]
    return cost, move

def parallelMax(board,startState,depth,captured,moving_piece,move_square):
    legal_moves = list(board.legal_moves)
    max_cores=1
    getNumCPu=os.cpu_count() or 1
    if getNumCPu >1:
        max_cores=max(getNumCPu-2,1)

    with ProcessPoolExecutor(max_workers=max_cores) as executor:
        args = [(board, startState, depth, move) for move in legal_moves]
        results = executor.map(evaluate_move_root, args)

    best_score = float('-inf')
    best_action = None
    for score, move in results:
        if score > best_score:
            best_score = score
            best_action = move

    return best_score, best_action

def maxValue(board,startState,depth,captured,moving_piece,move_square):
    #if len(board)==depth or borad.is_game_over():
    if depth==0 or board.is_game_over():

        return  add_postionValue(board,startState,captured,moving_piece,move_square),None

    bestMove=float('-inf')
    bestAction=None

    for actions in board.legal_moves:
        captured = board.piece_at(actions.to_square)
        moving_piece=board.piece_at(actions.from_square)

        board.push(actions)

        CostToMove=minValue(board,startState,depth-1,captured,moving_piece,actions.to_square)[0]
        #print("Maximizingvalues",CostToMove)

        board.pop()
        if CostToMove>bestMove:
           bestMove=CostToMove
           bestAction=actions
    #print("MaxValueChosen",bestMove)

    return bestMove,bestAction
    #simulating black is move
def minValue(board,startState,depth,captured,moving_piece,move_square):
    if  depth ==0 or board.is_game_over():

        return  add_postionValue(board,startState,captured,moving_piece,move_square),None
    worstMove=float('inf')
    worstAction=None

    for actions in board.legal_moves:
        captured = board.piece_at(actions.to_square)
        moving_piece=board.piece_at(actions.from_square)
        board.push(actions)
        costToMove=maxValue(board,startState,depth-1,captured,moving_piece,actions.to_square)[0]

        board.pop()
        #print("Minimizing values",costToMove)
        if worstMove>costToMove:
            worstMove=costToMove
            worstAction=actions

    #print("minValueChose",worstMove)

    return worstMove,worstAction



'''def WritenewGeneratedMoves():

     with open("add_postionValueMay4th.pkl","wb") as f:
         pickle.dump(positionValue,f)'''
