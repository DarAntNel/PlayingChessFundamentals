
import chess
#from EvalSnapshot import  add_postionValue
from EvaluatePositon import add_postionValue
#from NewIdeamay20_1109 import add_postionValue
#from Snpshot28_955 import add_postionValue # whins playmates easilly'''


positionValue=dict()
#with open("add_postionValueMay4th.pkl","rb") as f:
#    positionValue=pickle.load(f)


def findNextMove(board,startState, depth,captured,moving_piece,move_square):
         return maxValue(board,startState, depth,captured,moving_piece,move_square)[1]

def maxValue(board,startState,depth,captured,moving_piece,move_square):

    if  depth==0 or  board.is_game_over():

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
