import chess
import chess.svg
import chess.pgn
import chess.engine
import time
import webbrowser
import os
from MiniMax import findNextMove as Minimax
mates = [

   "6k1/8/5QK1/8/8/8/8/8 w - - 0 1",  # 0: King + Queen vs King (Mate in 1)
   "7k/4B3/6KN/8/8/8/8/8 w - - 0 1",  # 1: King +  Knight and Bishop   vs king (Mate in 1)

   "1k6/2R1N3/3K4/8/8/8/8/8 w - - 0 1",  # 3: King + knight and Rook vs King (Mate in 2)
   "1k6/8/2RKR3/8/8/8/8/8 w - - 0 1",  # 4: King + 2 Rook vs King (Mate in 2)
   "k7/1p6/1KP5/2N5/8/8/8/8 w - - 0 1"#,# 5 : Knight + Pawn (Mate in 2)
   #"R2BRK2/PPPP2PP/5B2/8/5q2/8/ppQ2ppp/r1b1rk2 w - - 0 1"
   #"1Bb3BN/R2Pk2r/1Q5B/4q2R/2bN4/4Q1BK/1p6/1bq1R1rb w - - 0 1"  # this is a very difficult mate And will note be used  in the final report  Mimmax  and stockfish halucinates here. LOL

]
'''mates =[
  "R2BRK2/PPPP2PP/5B2/8/5q2/8/ppQ2ppp/r1b1rk2 w - - 0 1" ]'''

#Stockfish needs to be installed on your system beofore you can  execute this file

chess_engine = r"C:\Users\justino.dasilva\Documents\Masters\Fundamentals F AI\Projects\stockfish\stockfish-windows-x86-64-avx2.exe"
gameMoves=chess.pgn.Game()
#board=chess.Board(fenValue)
svg_path=system=os.path.realpath('PLayEngine.html')
# thie line is added just to see the move  as they are bein played

def playMiniMax(depth=3):
    startState=board
    #time.sleep(1)

    MyPlay=Minimax(board,startState,depth,captured=None,moving_piece=None,move_square=None)


    count=1
    print(f"{count}.",board.san(MyPlay),end=' ')
    board.push(MyPlay)

    svg_path=system=os.path.realpath('PLayEngine.html')
    #time.sleep(1)
    #webbrowser.open('file://'+svg_path)
    while not board.is_game_over():
        with chess.engine.SimpleEngine.popen_uci(chess_engine) as engine:
            engine.configure({"UCI_LimitStrength":True,"UCI_Elo":1320})
            result = engine.play(board, chess.engine.Limit(time=0.1))
            stockfishMove=result.move
            captured=board.piece_at(stockfishMove.to_square)
            moving_piece=board.piece_at(stockfishMove.from_square)
            print(board.san(stockfishMove))#print move in  oin command, this allow for  game import  on lichess.org
            count=count+1
            board.push(stockfishMove)

            with open("test.svg", "w") as f:
                f.write(chess.svg.board(board))
            if board.is_checkmate():
                return "Oponent Wins"
            #time.sleep(1)

            startState=board
            MyPlay=Minimax(board,startState,depth,captured,moving_piece,stockfishMove.to_square)
            print(f"{count}.",board.san(MyPlay),end=' ')#print move in  oin command, this allow for  game import  on lichess.org
            board.push(MyPlay)

            with open("test.svg", "w") as f:
                f.write(chess.svg.board(board))
            if board.is_checkmate():
                return "Congratualtions you are vitorious"
            #time.sleep(1)
for item in mates:
    board=chess.Board(item)
    playMiniMax()






#
