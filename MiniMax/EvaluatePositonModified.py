import chess
import random
import pickle
import chess.svg
import webbrowser
import os
#board=chess.Board()


pieces = {'p': 1,'n': 3,'b': 3,'r': 5,'q': 9,'k': 0,'P': 1,'N': 3,'B': 3,'R': 5,'Q': 9,'K': 0 }
WhitePieces = {'P': 1,'N': 3,'B': 3,'R': 5,'Q': 9,'K': 0 }
BlackPieces = {'p': 1,'n': 3,'b': 3,'r': 5,'q': 9,'k': 0 }

NumberOFWhitePiecesAtStart = {'P': 0,'N': 0,'B': 0,'R': 0,'Q': 0,'K': 0}
NumberOfBlackPiecesAtStart = {'p': 0,'n': 0,'b': 0,'r': 0,'q': 0,'k': 0}

NumberOFWhitePiecesAtEnd = {'P': 0,'N': 0,'B': 0,'R': 0,'Q': 0,'K': 0}
NumberOfBlackPiecesAtEnd = {'p': 0,'n': 0,'b': 0,'r': 0,'q': 0,'k': 0}

WhiteCapuredPieceRemoved = {'P': 0,'N': 0,'B': 0,'R': 0,'Q': 0,'K': 0}# to calculate individual piece loss
BlackCapturedPiecesRemoved = {'p': 0,'n': 0,'b': 0,'r': 0,'q': 0,'k': 0}#to calculate individaual piece loss


positions =[square for square in chess.SQUARES]

Squarevalue=dict()
sol=[[],[],[],[],[],[],[],[]]

# checks to see if only white pieces is in a colum  this gives total control of the colum
# and increase shte positional value.
def  whitePasser(board,position):
    column_index=chess.square_file(position)
    for rank in range(8):  # 0 to 7 corresponds to ranks 1 to 8
        square = chess.square(column_index, rank)
        piece = board.piece_at(square)
        if piece and not piece.color:  # piece.color == False means it's black
            return False
    return True


def blackPasser(board, position):
    column_index=chess.square_file(position)
    for rank in range(8):  # Ranks 0 to 7 (1st to 8th rank)
        square = chess.square(column_index, rank)
        piece = board.piece_at(square)
        if  piece is not None and piece.color:  #    if a piece in in the column it must only be black eles we return  fasee
            return False
    return True
def kingIsDefended(state,king): #this has not been implemented  yet
    emptySquares=0
    WhiteSquare=0
    blackSquare=0

    attacks=state.attacks(king)
    for point in attacks:
        piece=state.piece_at(point)
        if piece is None:
            emptySquares=emptySquares+1
        elif f"{piece}" in WhitePieces:
            WhiteSquare=WhiteSquare+1
        else:
            blackSquare=blackSquare+1
        val=(WhiteSquare+1)-(blackSquare+1)+(emptySquares+1)/2

    return val


def getPieceRank(state,square):
    PieceAtSquare=state.piece_at(square)
    piece_moves=[]
    if f'{PieceAtSquare}' in  WhitePieces:
        if f'{PieceAtSquare}'=="P":
            val= chess.square_rank(square)+1
            if whitePasser(state,square):
                val=val*val#need to add value if it protected
            return val

        elif f'{PieceAtSquare}'=="K":
             val=kingIsDefended(state,square)#not implemented yet
             return val
        else:
            if state.turn==chess.BLACK:
                state.turn=chess.WHITE
                piece_moves = [move for move in state.legal_moves if move.from_square == square]
                state.turn=chess.BLACK
            else:
                piece_moves = [move for move in state.legal_moves if move.from_square == square]
            return len(piece_moves)+chess.square_rank(square)+1

    else:
        if f'{PieceAtSquare}'=="p":
            val= (8-chess.square_rank(square))
            if blackPasser(state,square):
                val=val*val#need to add value if it protected
            return val
        elif '{PieceAtSquare}'=="k":
             val=kingIsDefended(state)# not  implemente yet


             return -1
        else:
            if state.turn==chess.WHITE:
                state.turn=chess.BLACK
                piece_moves = [move for move in state.legal_moves if move.from_square == square]
                state.turn=chess.WHITE
            return len(piece_moves)+(8-chess.square_rank(square))









def add_postionValue(board,startState,captured,moving_piece,move_square):
   ValueOfWhitePiecesAtStart=0
   ValueOfBlackPiecesAtStart=0
   TotalWhiteRankAtStart=0
   TotalBlackRankAtStart=0
   TotalWhiteRankAtFinish=0
   TotalBlackRankAtFinish=0
   #get values for depth analysis start state
   for square in chess.SQUARES:
        PieceAtSquare= startState.piece_at(square)
        if f'{PieceAtSquare}' in WhitePieces:
            TotalWhiteRankAtStart=TotalWhiteRankAtStart+getPieceRank(startState,square)
            ValueOfWhitePiecesAtStart=WhitePieces[f'{PieceAtSquare}']+ValueOfWhitePiecesAtStart
            NumberOFWhitePiecesAtStart[f'{PieceAtSquare}']=NumberOFWhitePiecesAtStart[f'{PieceAtSquare}']+1

        elif  f'{PieceAtSquare}' in BlackPieces:
            TotalBlackRankAtStart=TotalBlackRankAtStart+getPieceRank(startState,square)
            ValueOfBlackPiecesAtStart=BlackPieces[f'{PieceAtSquare}']+ValueOfBlackPiecesAtStart
            NumberOfBlackPiecesAtStart[f'{PieceAtSquare}']=NumberOfBlackPiecesAtStart[f'{PieceAtSquare}']+1
   #print("startvalue",ValueOfWhitePiecesAtStart,ValueOfBlackPiecesAtStart)
   # finished getting values for deptj analysis




   if board.is_checkmate():

        if f'{moving_piece}' in WhitePieces:

            return 10000
        else:


            return -10000
   elif board.is_stalemate():
        if f'{moving_piece}' in WhitePieces:

            return 5000
        else:

            return -5000
   elif board.is_insufficient_material():
        if f'{moving_piece}' in WhitePieces:

            return 6000
        else:
            return -6000




   sol = [[] for _ in range(8)]
   whiteUndefendedAttacker=[]
   whitevalue=0
   blackvalue=0
   moves=board.legal_moves
   Turn=board.turn
   column=0
   row=0
   count=0

   AttackingPiece=None

   for target_square in positions:
        # find attacker and defenders
        blackking=None
        whiteking=None
        whitekingPosition=None
        blackkingPosition=None
        BlackTypeOfAttackers=[]
        WhiteTypeOfAttackers=[]
        rank=None
        total_whitevalue=0
        total_blackvalue=0

        white_attackers=board.attackers(chess.WHITE,target_square)
        black_attackers = board.attackers(chess.BLACK, target_square)

        AttackedPiece=board.piece_at(target_square)

        WhiteLength=len(white_attackers)
        BlackLength=len(black_attackers)


        for WhiteP in white_attackers:
            pice=board.piece_at(WhiteP)
            total_whitevalue=WhitePieces[f'{pice}']


        for BlackP in black_attackers:
            pice=board.piece_at(BlackP)
            total_blackvalue=BlackPieces[f'{pice}']




        WhiteReturn=0
        BlackReturn=0

        if board.turn==chess.WHITE:

            if captured is not None:
                 hello="lll"
            else:

                c=";;;"
                #print("White you are out the bushes")
        if board.turn==chess.BLACK:




            if f'{AttackedPiece}'in BlackPieces:
                #print("hello im a BlackPiece ", target_square,AttackedPiece)
                #BlackReturn=BlackReturn+BlackLength+total_blackvalue
                #WhiteReturn=WhiteReturn+WhiteLength+total_whitevalue
                if BlackLength>0 and WhiteLength>0 and BlackLength==WhiteLength:


                    BlackReturn=BlackLength+total_whitevalue
                    WhiteReturn=WhiteReturn+BlackPieces[f'{AttackedPiece}']+total_blackvalue//(1+BlackLength)

                if BlackLength>0 and WhiteLength>0 and BlackLength>WhiteLength:
                    #print("both More than 0 Before",target_square,BlackReturn,WhiteReturn)

                    BlackReturn=BlackLength+total_whitevalue+1
                    WhiteReturn=WhiteReturn+BlackPieces[f'{AttackedPiece}']
                    #print("both More than 0 After",target_square,BlackReturn,WhiteReturn)
                elif BlackLength>0 and WhiteLength==0:
                    #print("square:",target_square)
                    BlackReturn=BlackReturn+BlackPieces[f'{AttackedPiece}']+BlackLength
                elif BlackLength==0 and WhiteLength==0:
                    #print("square:",target_square)
                    BlackReturn=BlackReturn+BlackPieces[f'{AttackedPiece}']


                elif BlackLength==0 and WhiteLength>0:
                    WhiteReturn=WhiteReturn+WhiteLength+BlackPieces[f'{AttackedPiece}']






            if f'{AttackedPiece}' in WhitePieces:

                if BlackLength==WhiteLength and WhiteLength>0:

                    BlackReturn=BlackReturn+WhitePieces[f'{AttackedPiece}']+total_whitevalue//(1+WhiteLength)
                    WhiteReturn=WhiteReturn+total_blackvalue

                elif BlackLength==0 and WhiteLength==0:
                    WhiteReturn=WhiteReturn+WhitePieces[f'{AttackedPiece}']
                elif BlackLength==0 and WhiteLength>0:
                    WhiteReturn=WhiteReturn+WhiteLength+WhitePieces[f'{AttackedPiece}']#may be an overestimataion
                elif BlackLength>0 and WhiteLength==0:#black is attacking a piece that is note defended

                    BlackReturn=BlackReturn+WhitePieces[f'{AttackedPiece}']+1
                    if move_square==target_square:

                        if captured is not None:

                            #print("ssssssssssss",captured)
                            if WhitePieces[f'{moving_piece}']>BlackPieces[f'{captured}']:

                                BlackReturn=BlackReturn+WhitePieces[f'{moving_piece}']*2+BlackPieces[f'{captured}']+chess.square_rank(target_square)+1

                                #print("moving_piedddddddddddddddddddddddddddce",moving_piece,captured)

                    #if the piece being attacked is also attacking other blackpieces
                    board.turn=chess.WHITE
                    attacks=board.attacks(target_square)


                    for item in attacks:

                         currentpice=str(board.piece_at(item))

                         if currentpice in BlackPieces:

                              BlackReturn=BlackReturn+BlackPieces[currentpice]+1 # void the value of the attack as the the attacking piece is not defended

                         elif currentpice == 'None':
                            #print("before",BlackReturn)

                            BlackReturn=BlackReturn+1
                            #print("after",BlackReturn)

                    board.turn=chess.BLACK
            elif  AttackedPiece is None:
                  WhiteReturn=WhiteReturn+WhiteLength
                  BlackReturn=BlackLength
            if moving_piece =='k':
                b="fff"








             ##########################################################################

        sol[row].append(WhiteReturn-BlackReturn)
        #print("row: ",row,"column",column,"BlackReturn: ",BlackReturn,"WhiteReturn: ",WhiteReturn)
        if column==7:
           column=0
           row=row+1
        else:
           column=column+1


   ValueOfWhitePiecesAtFinish=0
   ValueOfBlackPiecesAtFinish=0
   #get values for depth analysis end state
   for square in chess.SQUARES:
        PieceAtSquare= board.piece_at(square)
        if f'{PieceAtSquare}' in WhitePieces:
            TotalWhiteRankAtFinish=TotalWhiteRankAtFinish+getPieceRank(board,square)
            ValueOfWhitePiecesAtFinish=WhitePieces[f'{PieceAtSquare}']+ValueOfWhitePiecesAtFinish
            NumberOFWhitePiecesAtEnd[f'{PieceAtSquare}']=NumberOFWhitePiecesAtEnd[f'{PieceAtSquare}']+1
        elif  f'{PieceAtSquare}' in BlackPieces:
            TotalBlackRankAtFinish=TotalBlackRankAtFinish+getPieceRank(board,square)
            ValueOfBlackPiecesAtFinish=BlackPieces[f'{PieceAtSquare}']+ValueOfBlackPiecesAtFinish
            NumberOfBlackPiecesAtEnd[f'{PieceAtSquare}']=NumberOfBlackPiecesAtEnd[f'{PieceAtSquare}']+1
    # finisishe getting deptht for analysis

   '''calculate rank of all  all pieces '''
   finishedWhiteRank=0
   finisheBlackrank=0
   whiteFinal=0
   blackFinal=0

   whiteFinal=whiteFinal -(TotalWhiteRankAtStart-TotalWhiteRankAtFinish)
   blackFinal=blackFinal+(TotalBlackRankAtStart-TotalBlackRankAtFinish)



   '''  finshed calculate rank of all pices '''


   #print("total losses",ValueOfWhitePiecesAtFinish,ValueOfBlackPiecesAtFinish,(ValueOfWhitePiecesAtStart-ValueOfWhitePiecesAtFinish),ValueOfBlackPiecesAtStart-ValueOfBlackPiecesAtFinish)
   whiteFinal=whiteFinal-(((ValueOfWhitePiecesAtStart-ValueOfWhitePiecesAtFinish)*(ValueOfWhitePiecesAtStart-ValueOfWhitePiecesAtFinish)*(ValueOfWhitePiecesAtStart-ValueOfWhitePiecesAtFinish))*.75)
   blackFinal=blackFinal+(((ValueOfBlackPiecesAtStart-ValueOfBlackPiecesAtFinish)*(ValueOfBlackPiecesAtStart-ValueOfBlackPiecesAtFinish)*(ValueOfBlackPiecesAtStart-ValueOfBlackPiecesAtFinish))*.75)



   total=0

   for item in sol:
       total= total+sum(item)



   '''for item in range(7,-1,-1):
          print(sol[item])
   print(total)'''


   total=total+whiteFinal+blackFinal

   return total

#print("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
Nxc7='r1bqkb1r/ppN1pp1p/2n2np1/3p4/8/5N2/PPPPPPPP/R1BQKBR1 b HQkq - 0 1'
board=chess.Board(Nxc7)
'''with open("test.svg", "w") as f:
    f.write(chess.svg.board(board))
webbrowser.open('file://' + os.path.realpath("test.svg"))
board1=chess.Board()
add_postionValue(board,board1,captured='p',moving_piece='N',move_square=50)'''

#for item in range(7,-1,-1):
#     print(sol[item])
#
