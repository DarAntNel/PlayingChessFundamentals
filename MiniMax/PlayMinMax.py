import chess
import sys
import time
board =chess.Board()
def findNextMove(board, player, depth):
    while not board.is_game_over():
        print("start",time.strftime("%H:%M:%S", time.localtime()))
        moveToMake = maxValue(board, depth)[1]
        print(f"White plays: {moveToMake}")
        board.push(moveToMake)
        print("finish",time.strftime("%H:%M:%S", time.localtime()))
        print(board)

        while True:
            oppInput = input("Black to move (in UCI format, e.g. e7e5): ").strip()
            try:
                oppMove = chess.Move.from_uci(oppInput)
                if oppMove in board.legal_moves:
                    board.push(oppMove)
                    break
                else:
                    print("Illegal move. Try again.")
            except:
                print("Invalid format. Try again.")



def maxValue(board,depth):


    legalmoves=list(board.legal_moves)

    if  depth==0 or  board.is_game_over():
        return  evaluateMove(board),None

    bestMove=float('-inf')
    bestAction=None

    for actions in legalmoves:
        board.push(actions)
        CostToMove=minValue(board,depth-1)[0]
        board.pop()
        if CostToMove>bestMove:
           bestMove=CostToMove
           bestAction=actions

    return bestMove,bestAction
    #simulating black is move
def minValue(board,depth):

    legalmoves=board.legal_moves
    #print(depth)

    if  depth ==0 or board.is_game_over():
        return  evaluateMove(board),None
    worstMove=float('inf')
    worstAction=None

    for actions in legalmoves:
        board.push(actions)
        costToMove=maxValue(board,depth-1)[0]
        board.pop()
        if worstMove>costToMove:
            worstMove=costToMove
            worstAction=actions

    return worstMove,worstAction



def evaluateMove(board):
    #return len(list(board.legal_moves))
    value=0
    legalmoves=board.legal_moves
    if len(list(legalmoves))==0:
      if board.is_checkmate():
           return -100

    elif board.is_stalemate()==True:
      return -10
    elif board.is_insufficient_material()==True:
      return -10
    else:
      pieceArray=(((str(legalmoves))[38:])[:-2]).split(',')
      i=0
      for actions in legalmoves:
          if pieceArray[i][0]=='Q':
              value=value+20
          elif pieceArray[i][0]=='N':
              value=value+8
          elif pieceArray[i][0]=='B':
              value=value+13
          elif pieceArray[i][0]=='R':
              value=value+14
          else:
              value=value+int(str(actions)[1])+1

    return value




depth=int(sys.argv[1])
#startingPostion=sys.argv[2]
startingPostion="5K1k/6pp/7n/3Q4/7N/8/8/8 w - - 0 1"
#board=chess.Board('r1bqkb1r/pppp1Qpp/2n2n2/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 4')
#board=chess.Board(startingPostion)
#print(dir(board))
legalMoves=board.legal_moves
count=0
'''for element in legalMoves:
     if count==0:
         board.push(element)
         print(board)
         count=count+1'''
pieceArray=(((str(board.legal_moves))[38:])[:-2]).split(',')
#strs=str(board.legal_moves)
#car=strs[38:]
#car1=car[:-2].split(',')
#print(dir(board))
#print(board)
#count=0
'''for element in board.legal_moves:

    #print(dir(element))
    #print(pieceArray[count][0])
    #print(str(element)[0])
    #print(dir(element.__getstate__))
    count=count+1'''
#[print(function) for function in dir(board)]

#[print(dir(functions)) for functions in board.legal_moves]

#[print(functions.__dataclass_params__) for functions in board.legal_moves]

player=1
findNextMove(board,'white',depth)

#
