import chess
import chess.svg
import chess.pgn
import chess.engine
import time
import webbrowser
import os
from MyMove import findNextMove
mates = [
    "6k1/8/8/8/8/8/5Q2/6K1 w - - 0 1",  # 0: King + Queen vs King (Mate in 1)
    "6k1/8/8/8/8/8/5R2/6K1 w - - 0 1",  # 1: King + Rook vs King (Mate in 1)
    "6k1/6P1/8/8/6B1/8/8/6K1 w - - 0 1",  # 2: King + Bishop + Pawn (Mate in 1)
    "6k1/8/8/8/8/5Q2/8/6K1 w - - 0 1",  # 3: King + Queen vs King (Mate in 2)
    "6k1/8/8/8/8/5R2/8/6K1 w - - 0 1",  # 4: King + Rook vs King (Mate in 2)
    "6k1/5P2/7K/8/8/5n2/8/8 w - - 0 1",  # 5: Knight + Pawn (Mate in 2)
    "6k1/8/8/8/8/4Q3/8/6K1 w - - 0 1",  # 6: King + Queen vs King (Mate in 3)
    "7k/8/8/8/8/8/5R2/6K1 w - - 0 1",  # 7: King + Rook vs King (Mate in 3)
    "6k1/8/8/3B4/8/8/6K1/8 w - - 0 1",  # 8: Bishop Mate (Mate in 3)
]



#from MyMove import WritenewGeneratedMoves
chess_engine = r"C:\Users\justino.dasilva\Documents\Masters\Fundamentals F AI\Projects\stockfish\stockfish-windows-x86-64-avx2.exe"
gameMoves=chess.pgn.Game()
board=chess.Board()
print("start",time.strftime("%H:%M:%S", time.localtime()))


for fenValue in  mates:
    board=chess.Board(fenValue)
    #MyPlay=findNextMove(board,2)
    '''//////////////// place you function here///////////////////////////////////////////////////////////'''
    if board.is_game_over():
        continue
    count=1
    print(f"{count}.",board.san(MyPlay),end=' ')
    board.push(MyPlay)
    svg_path=system=os.path.realpath('PlayingStockfish.html')
    webbrowser.open('file://'+svg_path)

    while True:
        with chess.engine.SimpleEngine.popen_uci(chess_engine) as engine:
            engine.configure({"UCI_LimitStrength":True,"UCI_Elo":1320})
            # Play a move from the starting position
            result = engine.play(board, chess.engine.Limit(time=0.1))
            stockfishMove=result.move
            time.sleep(1)
            print(board.san(stockfishMove))
            count=count+1
            board.push(stockfishMove)
            if  board.is_game_over():
                break;

            with open("test.svg", "w") as f:
                f.write(chess.svg.board(board))

            MyPlay=findNextMove(board,2)
            print(f"{count}.",board.san(MyPlay),end=' ')
            board.push(MyPlay)
            if board.is_game_over():
                break
            #gameMoves = gameMoves.add_variation(chess.Move.from_uci(f'{MyPlay}'))
            #print(board)
            with open("test.svg", "w") as f:
                f.write(chess.svg.board(board))
            #print(board)





#with open("game_output.pgn", "w") as pgn_file:
#    print(game, file=pgn_file)
#WritenewGeneratedMoves()
#print("totalTime Taken",time.strftime("%H:%M:%S", time.localtime()))
