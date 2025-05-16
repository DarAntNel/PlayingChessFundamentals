import chess
import random
import pickle
import chess.svg
import webbrowser
import os
#board=chess.Board()


pieces = {
    'p': 1,
    'n': 3,
    'b': 3,
    'r': 5,
    'q': 9,
    'k': 0,
    'P': 1,
    'N': 3,
    'B': 3,
    'R': 5,
    'Q': 9,
    'K': 0
}
WhitePieces = {
    'P': 1,
    'N': 3,
    'B': 3,
    'R': 5,
    'Q': 9,
    'K': 0
}
BlackPieces = {
    'p': 1,
    'n': 3,
    'b': 3,
    'r': 5,
    'q': 9,
    'k': 0,

}
betterhorse="rnbqkbnr/pp3pp1/2p5/3pp2p/8/1N6/PPPPPPPP/RNBQKB1R b KQkq - 1 5"
horsed7="rnbqkbnr/pp1N1pp1/2p5/3pp2p/8/8/PPPPPPPP/RNBQKB1R b KQkq - 1 5"
queentakesPawn="r1bqkb1r/ppp2pp1/2n2n1p/3pp1Q1/7P/4P3/PPPP1PP1/RNB1KBNR w KQkq - 0 6"
queensMovesback="r1bqkb1r/ppp2pp1/2n2n1p/3pp3/7P/4P1Q1/PPPP1PP1/RNB1KBNR b KQkq - 1 6"
wayBetter="rnbqkbnr/pppp1ppp/4p3/8/8/3P3N/PPP1PPPP/RNBQKB1R w KQkq - 0 1"
Stupid="rnbqkbnr/pppp1ppp/4p3/6N1/8/8/PPPPPPPP/RNBQKB1R w KQkq - 0 1"
positions =[square for square in chess.SQUARES]
kingAttackedNotDefended="7k/6P1/B7/8/8/8/8/6K1 w HAha - 0 1"
kingAttacked="7k/6P1/B4P2/8/8/8/8/6K1 w HAha - 0 1"
simmpleevaluation1="8/6Pk/B7/8/8/8/8/6K1 w - - 0 1"
simmpleevaluation2="8/6Pk/5K2/1B6/8/8/8/8 w HAha - 0 1"
betterMove="rnbqkbnr/pp1pppp1/2p4p/8/8/5N2/PPPPPPPP/RNBQKB1R b KQkq - 1 3"
foolishmove="rnbqkbnr/pp1ppppN/2p4p/8/8/8/PPPPPPPP/RNBQKB1R b KQkq - 1 3"
fen1="r1bqkb1r/ppp1pp1p/5np1/3p4/1P1P4/2NB1N2/P3PPPP/R1BQKB1R w KQkq - 0 61"
varient="r4bnr/pppk1p1p/4pqp1/3p4/1n6/N3PN1Q/PPPP1PPP/R1B1K2R b KQ - 1 9"
flawedcheck="r4bnr/pppk1p1p/4pqp1/3pN3/1n6/4P2Q/PPPP1PPP/RNB1K2R b KQ - 1 9"
fen2="8/2b3p1/6P1/1kpPp3/1p1pB1b1/1P1P2B1/2PK4/8 w HAha - 0 1"
eatingBlack="rnb1kbnr/p1pp1ppp/4p3/1p4q1/8/4P3/PPPP1PPP/RNBQKB1R w KQkq - 0 1"
eatingWhite="rnb1kbnr/pppp1ppp/4p3/6q1/8/8/PPPPPPPP/RNBQKB1R w KQkq - 0 3"
eatingless="2k3rr/1p1nNpp1/2pq4/p3p3/1b4QP/3PP1P1/PPP2P2/R1B2K2 w HQka - 0 1"
attackedForwardmove="r2qk1nr/ppp2Npp/2n2p2/3pp3/1b5P/1RN5/PPPPPPP1/R1BQK3 w Qkq - 0 1"
lessAponentAttacingHighervalue="rnbqkbnr/pp1p2pp/2p2p2/4p1N1/7P/8/PPPPPPP1/RNBQKB1R w KQkq - 0 4"
blackUnefended="r2qkbnr/p1pp1ppp/n2bp3/1B6/8/4P3/PPPP1PPP/RNBQK2R w KQkq - 0 1"
fen4="rnbqkbnr/p1pp1ppp/4p3/1p4N1/8/4P3/PPPP1PPP/RNBQKB1R w KQkq - 0 1"

mate1="6k1/8/5QK1/8/8/8/8/8 w - - 0 1"
mate="3Q2k1/8/6K1/8/8/8/8/8 b - - 0 1"
queenChecks="rnbqk1nr/ppppb1pp/5pQ1/4p3/8/2P2N2/PP1PPPPP/RNB1KB1R b KQkq - 1 4"
e4Instead="rnbqk1nr/ppppb1pp/5p2/4p3/4P3/2P2N2/PPQP1PPP/RNB1KB1R b KQkq - 0 4"
fenValue=e4Instead


'''board=chess.Board(fenValue)
with open("test.svg", "w") as f:
    f.write(chess.svg.board(board))
webbrowser.open('file://' + os.path.realpath("test.svg"))'''
Squarevalue=dict()
sol=[[],[],[],[],[],[],[],[]]
#def valueofPieceAtPostition()'''
def add_postionValue(board,captured,moving_piece,move_square):



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
        rank=None

        white_attackers=board.attackers(chess.WHITE,target_square)
        black_attackers = board.attackers(chess.BLACK, target_square)
        WhiteLength=len(white_attackers)
        BlackLength=len(black_attackers)

        rank=chess.square_rank(target_square)
        AttackedPiece=board.piece_at(target_square)
        if f'{AttackedPiece}' in BlackPieces:
            blackrank=8-chess.square_rank(target_square)
        elif f'{AttackedPiece}' in WhitePieces:
            whiterank=chess.square_rank(target_square)+1

        total_whitevalue=0
        total_blackvalue=0
        WhiteReturn=0
        BlackReturn=0
        # calculate the total value of the  white attackers by piece value
        for item in white_attackers:
            #if the white  king attacking the target square set  it value to True
            AttackingPiece=board.piece_at(item)
            if f'{AttackingPiece}'=='K':
                whiteking=True
            total_whitevalue=total_whitevalue+WhitePieces[f'{AttackingPiece}']

        #calculate the total value of the black_attackers by value of black pices


        for item in black_attackers:
            AttackingPiece=board.piece_at(item)
            if f'{AttackingPiece}'=='k':
                blackking=True
            total_blackvalue=total_blackvalue+BlackPieces[f'{AttackingPiece}']

        '''///////////////////////////Static board  evaluation//////////////////////////'''
        if f'{AttackedPiece}' in BlackPieces: # tThe square we are looking at has a black pice

             if f'{AttackedPiece}'=='p':
                 BlackReturn=BlackReturn+blackrank

             if WhiteLength==0 and BlackLength>0: #if no piece white piece is attacking its value
                BlackReturn=BlackReturn+total_blackvalue

             elif WhiteLength>0  and BlackLength==0:
                 #BlackReturn=BlackReturn-rank-BlackPieces[f'{AttackedPiece}']-total_whitevalue-(8-(rank-1))
                 BlackReturn=BlackReturn-BlackPieces[f'{AttackedPiece}']-total_whitevalue-blackrank-(8-(blackrank-1))
             #if white is more than 0 and  attacker is more than defender
             #add the diffrence to the attaker [white]

             elif WhiteLength>0 and WhiteLength-BlackLength>0:
                 # check attaker type
                 BlackReturn=BlackReturn-(WhiteLength-BlackLength)-(total_whitevalue-total_blackvalue)-blackrank-(8-(blackrank-1))#to be reassesses

             #if white has  attackers but black has defenders  add the
             #diffreence to the defenders{black}
             elif WhiteLength>0  and WhiteLength-BlackLength<0:
                 BlackReturn=BlackReturn+(BlackLength-WhiteLength)-BlackPieces[f'{AttackedPiece}']-blackrank-(8-(blackrank-1))-(total_whitevalue-total_blackvalue)
             #if the piece is neither attacked nor  defended  ad the
             #value of the piece in question plus increase its rank its no a hgher rank
             #elif WhiteLength==0 and BlackLength==0:
             if WhiteLength==0 and BlackLength==0:
                 #print("NO ONE Came her Black")
                 #print("testing Rank  isolated blaack",AttackedPiece,"on",target_square)
                 BlackReturn=BlackReturn+BlackPieces[f'{AttackedPiece}']
             #if the king is in check and has to move
             if WhiteLength==BlackLength:
                 BlackReturn=BlackReturn+total_blackvalue

             if f'{AttackedPiece}'=='k':
                 #print("black king in check")
                 BlackReturn=0



        #A White piece is on  square we are looking at
        if f'{AttackedPiece}' in WhitePieces:

            ## special cases  to consider
            if f'{AttackedPiece}'=='P':

                WhiteReturn=WhiteReturn+rank
            if f'{AttackedPiece}'=='K' and BlackLength==0:
                WhiteReturn=0#need to consider defending pices of attacers
            elif f'{AttackedPiece}'=='K' and WhiteLength:
                WhiteReturn=WhiteReturn+1
            elif f'{AttackedPiece}'!='K' and BlackLength==0 :
                #print("before",WhiteReturn)
                WhiteReturn=WhiteReturn+WhitePieces[f'{AttackedPiece}']
                #print("after",WhiteReturn)

            ######################## special cases

            #if the current pices is not being attacked by a black piece but its deended
            if BlackLength==0 and WhiteLength>0:

                WhiteReturn=WhiteReturn+total_whitevalue#add 1 for the piece itself
                #print("We are looking at a white piece",WhiteReturn)
            #if the current piece is being attacked but not being defended  reduce  by the pieve value
            elif BlackLength>0  and WhiteLength==0:
                WhiteReturn=WhiteReturn-WhitePieces[f'{AttackedPiece}']-total_blackvalue-whiterank-(8-(whiterank)+1)

            #ther are more black attackers  thanther are white defenders add value to the  black pieces
            elif BlackLength>0 and BlackLength-WhiteLength>0:
                WhiteReturn=WhiteReturn-(BlackLength-WhiteLength)-WhitePieces[f'{AttackedPiece}']-(total_blackvalue-total_whitevalue)-whiterank-((8-whiterank)+1)

            elif BlackLength>0 and BlackLength-WhiteLength<0:
                WhiteReturn=WhiteReturn+(WhiteLength-BlackLength) -WhitePieces[f'{AttackedPiece}']-(total_blackvalue-total_whitevalue)-whiterank-(8-(whiterank)+1)
            #if the pice is isolated  it is neither defended not AttackedPiece
            elif BlackLength==0 and WhiteLength==0:# dont allow a pice to go our isolated

                WhiteReturn=WhiteReturn+WhitePieces[f'{AttackedPiece}']
            elif BlackLength>0 and WhiteLength>0 and WhiteLength==BlackLength:
                WhiteReturn=WhiteReturn-total_whitevalue-(8-(whiterank-1))-WhitePieces[f'{AttackedPiece}']




        '''//////////////////////////Static evaluation if the board//////////////////'''


        if target_square==move_square and captured!=None:

            if f'{captured}' in WhitePieces:# Black just captured a white piece  give value to black
                # if white is not defending the pice that was captured reduce it valu
                    #move=board.peek()
                    rank=8-chess.square_rank(move_square)
                    WhiteReturn=WhiteReturn-WhitePieces[f'{captured}']*2-BlackPieces[f'{moving_piece}']-rank



            elif f'{captured}' in BlackPieces:# Black just captured a white piece  give value to black
                # if white is not defending the pice that was captured reduce it valu
                    #move=board.peek()
                    rank=chess.square_rank(move_square)+1
                    BlackReturn=BlackReturn-BlackPieces[f'{captured}']*2-WhitePieces[f'{moving_piece}']-rank

        if target_square==move_square and captured==None:
            if f'{moving_piece}' in WhitePieces:#a white pices just moved its black turn to moved
                if WhiteLength==0 and BlackLength>0:
                    rank=chess.square_rank(move_square)+1#get the white rank it a white piece that moved
                    WhiteReturn=(WhiteReturn-WhitePieces[f'{moving_piece}']-rank-total_blackvalue)*2#pubish white evaluantion for makin a bad move
                    #remove teh value of all pieces it attacks.
                    #valueofPieceAtPostition=

            elif f'{moving_piece}' in BlackPieces:# black just moved  if white to move
                #print("enteer here",move_square)
                if BlackLength==0 and WhiteLength>0:
                    rank=8-chess.square_rank(move_square)
                    BlackReturn=(BlackReturn-BlackPieces[f'{moving_piece}']-rank-total_whitevalue)*2

        #check what pieces th las aponent move is ataacking

















             # if the number of  protector is more than add the toal number of protectors














        sol[row].append(WhiteReturn-BlackReturn)
        if column==7:
           column=0
           row=row+1
        else:
           column=column+1
   total=0
   for item in sol:
       total= total+sum(item)
   #print(total)
   #print(board)
   '''for item in range(7,-1,-1):
        print(sol[item])
   print(total)'''
   return abs(total)

#add_postionValue(board,captured='None',moving_piece='Q',move_square=46)

#for item in range(7,-1,-1):
#     print(sol[item])
#
