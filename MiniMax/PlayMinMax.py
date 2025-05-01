import chess
import sys
import time
board=chess.Board()
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

    if  depth==0 or  board.is_game_over():
        return  evaluateMove(board),None

    bestMove=float('-inf')
    bestAction=None

    for actions in board.legal_moves:
        board.push(actions)
        CostToMove=minValue(board,depth-1)[0]
        board.pop()
        if CostToMove>bestMove:
           bestMove=CostToMove
           bestAction=actions

    return bestMove,bestAction
    #simulating black is move
def minValue(board,depth):
    if  depth ==0 or board.is_game_over():
        return  evaluateMove(board),None
    worstMove=float('inf')
    worstAction=None

    for actions in board.legal_moves:
        board.push(actions)
        costToMove=maxValue(board,depth-1)[0]
        board.pop()
        if worstMove>costToMove:
            worstMove=costToMove
            worstAction=actions

    return worstMove,worstAction



def evaluateMove(board):
    #pieces={'Pawn':1,'Rook':5,'Bishop':3,'Knight':3,'Queeen':9,'King':0}
    value=0
    if board.is_checkmate():
        if board.turn==chess.WHITE:
            return -100
        else:
            return +100

    elif board.is_stalemate()==True:
        if board.turn==chess.WHITE:
            return +10
        else:
            return -10


    elif board.is_insufficient_material()==True:
      if board.turn==chess.WHITE:
          return +10
      else:
          return -10
    else:
        last_move=str(board.peek())
        last_move1=board.peek()
        piece=board.piece_at(last_move1.to_square)
        #print(last_move[-2:])
        column=last_move[-2]
        row=last_move[-1]
        if piece==1:
            value=1+int(row)
            if int(column)=='h' or colum=='a':
                value=value+1
            if board.is_capture(last_move)==True:
                value=value+2



        elif piece==2:
            if last_move[-2:] in ['a1','a8','h1','h8']:
                value=value+2
            #determine if ther was a  capture==# TODO:

            elif last_move[-2:] in ['b1','b8','g1','g8','a2','h2','a7','h7']:
                value=value+3
            elif last_move[-2:] in ['b2','c1','d1','e1','f1','g2','b7','c8','d8','e8','f8','g7','a3','a4','a5','a6','h3','h4','h5','h6']:
                value=value+4
            elif last_move[-2:] in ['c2','d2','e2','f2','c7','d7','e7','f7','b3','b4','b5','b6','g3','g4','g5','g6']:
                value=value+6
            else:
                value=value+8



        elif piece==3:
            if last_move[-2:] in ['c1','a3','f1','h3','a6','c8','f8','h6','a2','a7','h2','h7']:
                value=value+7
            elif last_move[-2:] in ['b2','b7','g2','g7','c2','d2','e2','f2','c7','d7','e7','f7','b3','b4','b5','b6','g3','g4','g5','g6']:
                value=value+9
            elif last_move[-2:] in ['d5','e5','d4','e4']:
                value=value+13
            else:
                value=value+11
        elif piece==4:
            #if last_move[-2:] in ['a1','b1','c1','d1','e1','f1','g1','h1','h2','h2','h4','h4','h6','h7','h8','g8','f8','e8','d8','c8','b8','a8']:
            vlaue=value+14
        elif piece==5:
            if last_move[-2:] in ['a1','b1','c1','d1','e1','f1','g1','h1','h2','h2','h4','h4','h6','h7','h8','g8','f8','e8','d8','c8','b8','a8']:
                value=value+21
            elif last_move[-2:] in ['b2','b3','b4','b5','b6','b7','c2','d2','e2','f2','g2','g3','g4','g5','g6','g7','f7','e7','d7','c7']:
                value=value+23
            elif last_move[-2:] in ['d5','e5','d4','e4']:
                value=value+27
            else:
                value=value+25
        else:
            if last_move[-2:] in ['a1','h1','a8','h8']:
                value=value+3
            elif last_move[-2:] in ['b1','c1','d1','e1','f1','g1','h2','h4','h6','h7','g8','f8','e8','d8','c8','b8']:
                value=value+5
            else:
                value=value+8







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
