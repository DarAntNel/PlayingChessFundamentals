
import chess
#from NewIdeamay20_1109 import  add_postionValue
from EvaluatePositon import add_postionValue
positionValue=dict()
#with open("add_postionValueMay4th.pkl","rb") as f:
#    positionValue=pickle.load(f)


def findNextMove(board,startState, depth,captured,moving_piece,move_square):
         return maxOfAverage(board,startState, depth,captured,moving_piece,move_square)[1]

def maxOfAverage(board,startState,depth,captured,moving_piece,move_square):

    if  depth==0 or  board.is_game_over():
        #print("turn=White",board.turn==chess.WHITE)
        return  add_postionValue(board,startState,captured,moving_piece,move_square),None

    bestMove=float('-inf')
    bestAction=None

    for actions in board.legal_moves:
        captured = board.piece_at(actions.to_square)
        moving_piece=board.piece_at(actions.from_square)
        board.push(actions)
        CostToMove=averageMove(board,startState,depth-1,captured,moving_piece,actions.to_square)[0]
        board.pop()
        if CostToMove>bestMove:
           bestMove=CostToMove
           bestAction=actions

    return bestMove,bestAction
    #simulating black is move
def averageMove(board,startState,depth,captured,moving_piece,move_square):
    if  depth ==0 or board.is_game_over():
        return  add_postionValue(board,startState,captured,moving_piece,move_square),None
    worstMove=float('inf')
    worstAction=None
    total=0
    for actions in board.legal_moves:
        captured = board.piece_at(actions.to_square)
        moving_piece=board.piece_at(actions.from_square)
        board.push(actions)
        costToMove=maxOfAverage(board,startState,depth-1,captured,moving_piece,actions.to_square)[0]
        board.pop()
        total=total+costToMove

    return total/len(list(board.legal_moves)),None



'''def WritenewGeneratedMoves():

     with open("add_postionValueMay4th.pkl","wb") as f:
         pickle.dump(positionValue,f)'''
