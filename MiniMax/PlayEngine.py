import chess
import chess.svg
import chess.pgn
import chess.engine
import time
import webbrowser
import os
import sys

from MimiMax import findNextMove as Minimax
from Expectimax import findNextMove as Expecti
from AphaBeta import findNextMove as Alpha



#from MyMove import WritenewGeneratedMoves

chess_engine = r"C:\Users\justino.dasilva\Documents\Masters\Fundamentals F AI\Projects\stockfish\stockfish-windows-x86-64-avx2.exe"
gameMoves=chess.pgn.Game()
board=chess.Board()
print("start",time.strftime("%H:%M:%S", time.localtime()))



count=1
def playMiniMax(depth=3):
    MyPlay=Minimax(board,depth,captured=None,moving_piece=None,move_square=None)
    count=1
    print(f"{count}.",board.san(MyPlay),end=' ')
    board.push(MyPlay)
    svg_path=system=os.path.realpath('PlayingStockfish.html')
    webbrowser.open('file://'+svg_path)
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

            MyPlay=Minimax(board,depth,captured,moving_piece,stockfishMove.to_square)
            print(f"{count}.",board.san(MyPlay),end=' ')
            board.push(MyPlay)

            with open("test.svg", "w") as f:
                f.write(chess.svg.board(board))
            if board.is_checkmate():
                return "Congratualtions you are vitorious"
def playAlphaBeta(depth=3):
    MyPlay=Alpha(board,depth,captured=None,moving_piece=None,move_square=None)
    count=1
    print(f"{count}.",board.san(MyPlay),end=' ')
    board.push(MyPlay)
    svg_path=system=os.path.realpath('PlayingStockfish.html')


    webbrowser.open('file://'+svg_path)
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

            MyPlay=Alpha(board,depth,captured,moving_piece,stockfishMove.to_square)
            print(f"{count}.",board.san(MyPlay),end=' ')
            board.push(MyPlay)

            with open("test.svg", "w") as f:
                f.write(chess.svg.board(board))
            if board.is_checkmate():
                return "Congratualtions you are vitorious"


def playExpectimax(depth=3):
    MyPlay=Expecti(board,depth,captured=None,moving_piece=None,move_square=None)
    count=1
    print(f"{count}.",board.san(MyPlay),end=' ')
    board.push(MyPlay)
    svg_path=system=os.path.realpath('PlayingStockfish.html')


    webbrowser.open('file://'+svg_path)
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

            MyPlay=Expecti(board,depth,captured,moving_piece,stockfishMove.to_square)
            print(f"{count}.",board.san(MyPlay),end=' ')
            board.push(MyPlay)

            with open("test.svg", "w") as f:
                f.write(chess.svg.board(board))
            if board.is_checkmate():
                return "Congratualtions you are vitorious"

if __name__ == "__main__":
    depth=int(sys.argv[1])
    agent=sys.argv[2]
    print("Usage: Depth, agent")

    if agent=='ExpectiMax':
        playExpectimax(depth)
    elif agent=='AlphaBeta':
        playAlphaBeta(depth)
    elif agent=='MiniMax':
        playMiniMax(depth)
    else:
        print(" incorrect input Usage example: python 3 MimiMax")





'''with open("game_output.pgn", "w") as pgn_file:
    print(game, file=pgn_file)
WritenewGeneratedMoves()'''

print("totalTime Taken",time.strftime("%H:%M:%S", time.localtime()))
