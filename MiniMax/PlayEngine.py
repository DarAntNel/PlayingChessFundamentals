import chess
import chess.svg
import chess.pgn
import chess.engine
import time
import webbrowser
import os
import sys

from MiniMax import findNextMove as Minimax
from ExpectiMax import findNextMove as Expecti
from AphaBeta import findNextMove as Alpha
#from MiniMaxParallel import maxValue as par


chess_engine = r"C:\Users\justino.dasilva\Documents\Masters\Fundamentals F AI\Projects\stockfish\stockfish-windows-x86-64-avx2.exe"
gameMoves=chess.pgn.Game()
board=chess.Board()





print("start",time.strftime("%H:%M:%S", time.localtime()))

count=1
def playMiniMax(depth=3):
    startState=board
    MyPlay=Minimax(board,startState,depth,captured=None,moving_piece=None,move_square=None)
    count=1
    print(f"{count}.",board.san(MyPlay),end=' ')
    board.push(MyPlay)

    svg_path=system=os.path.realpath('PLayEngine.html')
    #webbrowser.open('file://'+svg_path)
    while not board.is_game_over():
        with chess.engine.SimpleEngine.popen_uci(chess_engine) as engine:
            engine.configure({"UCI_LimitStrength":True,"UCI_Elo":1320})
            result = engine.play(board, chess.engine.Limit(time=0.1))
            stockfishMove=result.move
            captured=board.piece_at(stockfishMove.to_square)
            moving_piece=board.piece_at(stockfishMove.from_square)
            print(board.san(stockfishMove))
            count=count+1
            board.push(stockfishMove)

            with open("test.svg", "w") as f:
                f.write(chess.svg.board(board))
            if board.is_checkmate():
                return "Oponent Wins"
            startState=board
            MyPlay=Minimax(board,startState,depth,captured,moving_piece,stockfishMove.to_square)
            print(f"{count}.",board.san(MyPlay),end=' ')
            board.push(MyPlay)

            with open("test.svg", "w") as f:
                f.write(chess.svg.board(board))
            if board.is_checkmate():
                return "Congratualtions you are vitorious"
#parallel
def playpar(depth=3):
    MyPlay=par(board,depth,captured=None,moving_piece=None,move_square=None)
    count=1
    print(f"{count}.",board.san(MyPlay),end=' ')
    board.push(MyPlay)
    svg_path=system=os.path.realpath('PLayEngine.html')
    #webbrowser.open('file://'+svg_path)
    while not board.is_game_over():
        with chess.engine.SimpleEngine.popen_uci(chess_engine) as engine:
            engine.configure({"UCI_LimitStrength":True,"UCI_Elo":1320})
            result = engine.play(board, chess.engine.Limit(time=0.1))
            stockfishMove=result.move
            captured=board.piece_at(stockfishMove.to_square)
            moving_piece=board.piece_at(stockfishMove.from_square)
            print(board.san(stockfishMove))
            count=count+1
            board.push(stockfishMove)

            with open("test.svg", "w") as f:
                f.write(chess.svg.board(board))
            if board.is_checkmate():
                return "Oponent Wins"

            MyPlay=par(board,depth,captured,moving_piece,stockfishMove.to_square)
            print(f"{count}.",board.san(MyPlay),end=' ')
            board.push(MyPlay)

            with open("test.svg", "w") as f:
                f.write(chess.svg.board(board))
            if board.is_checkmate():
                return "Congratualtions you are vitorious"
#parallel

def playAlphaBeta(depth=3):
    startState=board
    MyPlay=Alpha(board,startState,depth,captured=None,moving_piece=None,move_square=None)
    count=1
    print(f"{count}.",board.san(MyPlay),end=' ')
    board.push(MyPlay)
    svg_path=system=os.path.realpath('PLayEngine.html')


    #webbrowser.open('file://'+svg_path)
    while not board.is_game_over():
        with chess.engine.SimpleEngine.popen_uci(chess_engine) as engine:
            engine.configure({"UCI_LimitStrength":True,"UCI_Elo":1320})
            result = engine.play(board, chess.engine.Limit(time=0.1))
            stockfishMove=result.move
            captured=board.piece_at(stockfishMove.to_square)
            moving_piece=board.piece_at(stockfishMove.from_square)
            print(board.san(stockfishMove))
            count=count+1
            board.push(stockfishMove)

            with open("test.svg", "w") as f:
                f.write(chess.svg.board(board))
            if board.is_checkmate():
                return "Oponent Wins"

            MyPlay=Alpha(board,startState,depth,captured=None,moving_piece=None,move_square=None)
            print(f"{count}.",board.san(MyPlay),end=' ')
            board.push(MyPlay)

            with open("test.svg", "w") as f:
                f.write(chess.svg.board(board))
            if board.is_checkmate():
                return "Congratualtions you are vitorious"


def playExpectimax(depth=3):
    startState=board
    MyPlay=Expecti(board,startState,depth,captured=None,moving_piece=None,move_square=None)
    count=1
    print(f"{count}.",board.san(MyPlay),end=' ')
    board.push(MyPlay)
    svg_path=system=os.path.realpath('PLayEngine.html')


    #webbrowser.open('file://'+svg_path)
    while not board.is_game_over():
        with chess.engine.SimpleEngine.popen_uci(chess_engine) as engine:
            engine.configure({"UCI_LimitStrength":True,"UCI_Elo":1320})
            result = engine.play(board, chess.engine.Limit(time=0.1))
            stockfishMove=result.move
            captured=board.piece_at(stockfishMove.to_square)
            moving_piece=board.piece_at(stockfishMove.from_square)
            print(board.san(stockfishMove))

            count=count+1
            board.push(stockfishMove)

            with open("test.svg", "w") as f:
                f.write(chess.svg.board(board))
            if board.is_checkmate():
                return "Oponent Wins"
            startState=board
            MyPlay=Expecti(board,startState,depth,captured,moving_piece,stockfishMove.to_square)
            print(f"{count}.",board.san(MyPlay),end=' ')
            board.push(MyPlay)

            with open("test.svg", "w") as f:
                f.write(chess.svg.board(board))
            if board.is_checkmate():
                return "Congratualtions you are vitorious"




if __name__ == "__main__":
    agent=sys.argv[1]
    depth=int(sys.argv[2])
    print("Usage: Agent depth",agent,depth)

    if agent=='ExpectiMax':
        playExpectimax(depth)
    elif agent=='AlphaBeta':
        playAlphaBeta(depth)
    elif agent=='MiniMax':
        playMiniMax(depth)
    elif agent=="par":
        playpar(depth)
    else:

        print(" incorrect input Usage example: python MiniMax 3")





'''with open("game_output.pgn", "w") as pgn_file:
    print(game, file=pgn_file)
WritenewGeneratedMoves()'''

print("totalTime Taken",time.strftime("%H:%M:%S", time.localtime()))
