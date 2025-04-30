import chess
import sys
board =chess.Board()
#[Hello Hello Hello]
#[print(functions) for functions in dir(board)]
#[print(functions) for functions in dir(board)]

legalmoves=board.legal_moves
print(board.pawns)
print(board)
#NF3=chess.Move.from_uci("g1f3")
#print(board._generate_evasions())
#board.push(NF3)
def findNextMove(board,player,depth):

    print("jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj")
    ##while not board.is_stalemate() or  not board.is_insufficient_material() or not board.is_checkmate():
    moveTomake=maxValue(board,player,depth)[1]
    board.push(moveTomake)
    legalMoves=board.legal_moves
    oppnentMove=None


    #while oppnentMove not in legalMoves:
    #    oppnentMove=input("Its your turn").strip()

    #    board.push(oppnentMove)





def maxValue(board,player,depth):
            legalmoves=[action for action in board.legal_moves]
            print(depth,len(legalmoves))
            if  len(legalmoves)==0 or depth==0 or board.is_stalemate() or board.is_insufficient_material() or board.is_game_over():
              return  evaluateMove(board,player),None

            #legalmoves=board.legal_moves
            bestMove=float('-inf')
            bestAction=None

            for actions in legalmoves:

                #play=chess.Move.from_uci(actions)
                board.push(actions)
                #print(board,"\n\n")
                nextDepth=depth

                CostToMove=minValue(board,player,nextDepth)[0]
                board.pop()
                if CostToMove>bestMove:
                   bestMove=CostToMove
                   bestAction=actions

            return bestMove,bestAction
    #black is moving
def minValue(board,player,depth):
        legalmoves=[action for action in board.legal_moves]
        if  len(legalmoves)==0 or board.is_stalemate() or board.is_insufficient_material() or board.is_checkmate():
             return  evaluateMove(board,player),None
        worstMove=float('inf')
        worstAction=None
        for actions in legalMoves:
            #play=board.Move.from_uci(actions)
            board.push(actions)
            nextDepth=depth-1
            CostToMove=maxValue(board,player-1,nextDepth)[0]
            #print(CostToMove)
            board.pop()
            if worstMove>CostToMove:
                worstMove=CostToMove
                worstAction=actions

        return worstMove,worstAction
def evaluateMove(board,player):
     value=0
     legalmoves=board.legal_moves
     if legalmoves==0:
          if board.is_chackmate():
               return -100

     elif board.is_stalemate()==True:
          return -10
     elif board.is_insufficient_material()==True:
          return -10
     else:
          pieceArray=(((str(legalMoves))[38:])[:-2]).split(',')
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
#pieceArray=(((str(board.legal_moves))[38:])[:-2]).split(',')
#strs=str(board.legal_moves)
#car=strs[38:]
#car1=car[:-2].split(',')
#count=0
'''for element in board.legal_moves:

    print(dir(element))
    print(pieceArray[count][0],)
    print(str(element)[0])
    count=count+1'''
#[print(function) for function in dir(board)]

#[print(dir(functions)) for functions in board.legal_moves]

#[print(functions.__dataclass_params__) for functions in board.legal_moves]

player=1
findNextMove(board,player,depth)
print(board.pawns,board.bishops)
#print(board.is_checkmate())
#
