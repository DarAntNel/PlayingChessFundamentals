import chess
import chess.svg
import chess.pgn
import chess.engine
import time
import webbrowser
import os
import sys
import copy
import concurrent.futures
from MiniMax import findNextMove as Minimax
from ExpectiMax import findNextMove as Expecti
from AphaBeta import findNextMove as Alpha
#from MiniMaxParallel import maxValue as par


chess_engine = r"C:\Users\justino.dasilva\Documents\Masters\Fundamentals F AI\Projects\stockfish\stockfish-windows-x86-64-avx2.exe"
gameMoves=chess.pgn.Game()
board=chess.Board()





print("start",time.strftime("%H:%M:%S", time.localtime()))

count=1
def playMiniMax(depth=3,ShowMoves=True,board=None):
    if board==None:
        board=chess.Board()
    startState=board
    MyPlay=Minimax(board,startState,depth,captured=None,moving_piece=None,move_square=None)
    count=1

    if ShowMoves==True:
        print(f"{count}.",board.san(MyPlay),end=' ')
        svg_path=system=os.path.realpath('PLayEngine.html')
    board.push(MyPlay)

    while not board.is_game_over():
        with chess.engine.SimpleEngine.popen_uci(chess_engine) as engine:
            engine.configure({"UCI_LimitStrength":True,"UCI_Elo":1320})
            result = engine.play(board, chess.engine.Limit(time=0.1))
            stockfishMove=result.move
            captured=board.piece_at(stockfishMove.to_square)
            moving_piece=board.piece_at(stockfishMove.from_square)
            if ShowMoves==True:
                count=count+1
                with open("test.svg", "w") as f:
                    f.write(chess.svg.board(board))
                print(board.san(stockfishMove))
            board.push(stockfishMove)#make the move

            if board.is_game_over():
                outcome=board.outcome()
                result = "Draw" if outcome.winner is None else ("White wins" if outcome.winner else "Black wins")
                if ShowMoves!=True:
                    with open("result.txt","a") as f:#write result to file
                        f.write(f"\n{result} by {outcome.termination.name}\n")
                break
            startState=board#removeStatement after testing is finished leave at beginning only
            MyPlay=Minimax(board,startState,depth,captured,moving_piece,stockfishMove.to_square)
            if ShowMoves==True:
                print(f"{count}.",board.san(MyPlay),end=' ')
                with open("test.svg", "w") as f:
                    f.write(chess.svg.board(board))
            board.push(MyPlay)



            if board.is_game_over():
                outcome=board.outcome()
                result = "Draw" if outcome.winner is None else ("White wins" if outcome.winner else "Black wins")
                if ShowMoves!=True:
                    with open("result.txt","a") as f:#write result to file
                        f.write(f"\n{result} by {outcome.termination.name}\n")
                    break
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
            if board.is_game_over():
                with open("result.txt","a") as f:#write result to file
                    f.write("\n",board.outcome())
                    break

            MyPlay=par(board,depth,captured,moving_piece,stockfishMove.to_square)
            print(f"{count}.",board.san(MyPlay),end=' ')
            board.push(MyPlay)

            with open("test.svg", "w") as f:
                f.write(chess.svg.board(board))
            if board.is_game_over():
                with open("result.txt","a"):#write result to file
                    file.write("\n",board.outcome())
                    break
#parallel

def playAlphaBeta(depth=3,ShowMoves=True,board=None):
    if board==None:
        board=chess.Board()
    startState=board
    MyPlay=Alpha(board,startState,depth,captured=None,moving_piece=None,move_square=None)
    count=1

    if ShowMoves==True:
        print(f"{count}.",board.san(MyPlay),end=' ')
        svg_path=system=os.path.realpath('PLayEngine.html')
    board.push(MyPlay)

    while not board.is_game_over():
        with chess.engine.SimpleEngine.popen_uci(chess_engine) as engine:
            engine.configure({"UCI_LimitStrength":True,"UCI_Elo":1320})
            result = engine.play(board, chess.engine.Limit(time=0.1))
            stockfishMove=result.move
            captured=board.piece_at(stockfishMove.to_square)
            moving_piece=board.piece_at(stockfishMove.from_square)
            if ShowMoves==True:
                count=count+1
                with open("test.svg", "w") as f:
                    f.write(chess.svg.board(board))
                print(board.san(stockfishMove))
            board.push(stockfishMove)#make the move

            if board.is_game_over():
                outcome=board.outcome()
                result = "Draw" if outcome.winner is None else ("White wins" if outcome.winner else "Black wins")
                if ShowMoves!=True:
                    with open("resultAB.txt","a") as f:#write result to file
                        f.write(f"\n{result} by {outcome.termination.name}\n")
                break
            startState=board#removeStatement after testing is finished leave at beginning only
            MyPlay=Alpha(board,startState,depth,captured,moving_piece,stockfishMove.to_square)
            if ShowMoves==True:
                print(f"{count}.",board.san(MyPlay),end=' ')
                with open("test.svg", "w") as f:
                    f.write(chess.svg.board(board))
            board.push(MyPlay)



            if board.is_game_over():
                outcome=board.outcome()
                result = "Draw" if outcome.winner is None else ("White wins" if outcome.winner else "Black wins")
                if ShowMoves!=True:
                    with open("resultAB.txt","a") as f:#write result to file
                        f.write(f"\n{result} by {outcome.termination.name}\n")
                    break


def playExpectimax(depth=3,ShowMoves=True,board=None):
    if board==None:
        board=chess.Board()
    startState=board
    MyPlay=Expecti(board,startState,depth,captured=None,moving_piece=None,move_square=None)
    count=1

    if ShowMoves==True:
        print(f"{count}.",board.san(MyPlay),end=' ')
        svg_path=system=os.path.realpath('PLayEngine.html')
    board.push(MyPlay)

    while not board.is_game_over():
        with chess.engine.SimpleEngine.popen_uci(chess_engine) as engine:
            engine.configure({"UCI_LimitStrength":True,"UCI_Elo":1320})
            result = engine.play(board, chess.engine.Limit(time=0.1))
            stockfishMove=result.move
            captured=board.piece_at(stockfishMove.to_square)
            moving_piece=board.piece_at(stockfishMove.from_square)
            if ShowMoves==True:
                count=count+1
                with open("test.svg", "w") as f:
                    f.write(chess.svg.board(board))
                print(board.san(stockfishMove))
            board.push(stockfishMove)#make the move

            if board.is_game_over():
                outcome=board.outcome()
                result = "Draw,Draw," if outcome.winner is None else ("White,wins," if outcome.winner else "Black,wins,")
                if ShowMoves!=True:
                    with open("resultExpecti.csv","a") as f:#write result to file
                        f.write(f"\n{result}by,{outcome.termination.name}\n")
                break
            startState=board#removeStatement after testing is finished leave at beginning only
            MyPlay=Expecti(board,startState,depth,captured,moving_piece,stockfishMove.to_square)
            if ShowMoves==True:
                print(f"{count}.",board.san(MyPlay),end=' ')
                with open("test.svg", "w") as f:
                    f.write(chess.svg.board(board))
            board.push(MyPlay)



            if board.is_game_over():
                outcome=board.outcome()
                result = "Draw,Draw," if outcome.winner is None else ("White,wins," if outcome.winner else "Black,wins")
                if ShowMoves!=True:
                    with open("resultExpecti.csv","a") as f:#write result to file
                        f.write(f"\n{result}by,{outcome.termination.name}\n")
                    break




if __name__ == "__main__":

    agent=sys.argv[1]
    depth=int(sys.argv[2])
    if len(sys.argv)==4:
        NumberOfIterations=int(sys.argv[3])
    else:
        NumberOfIterations=1

    if NumberOfIterations==1:
        ShowMoves=True
    else:
        #print("NumberOfIterations",NumberOfIterations)
        ShowMoves=False
    #playAlphaBeta(depth,ShowMoves,chess.Board())
    try:
        if agent=='ExpectiMax':
            with concurrent.futures.ProcessPoolExecutor(max_workers=6) as executor:
                futures = [executor.submit(playExpectimax, depth, ShowMoves,copy.deepcopy(chess.Board())) for _ in range(NumberOfIterations)]
                results = [f.result() for f in concurrent.futures.as_completed(futures)]
        elif agent=='AlphaBeta':
            with concurrent.futures.ProcessPoolExecutor(max_workers=6) as executor:
                futures = [executor.submit(playAlphaBeta, depth, ShowMoves,copy.deepcopy(chess.Board())) for _ in range(NumberOfIterations)]
                results = [f.result() for f in concurrent.futures.as_completed(futures)]


        elif agent == 'MiniMax':

            with concurrent.futures.ProcessPoolExecutor(max_workers=6) as executor:
                futures = [executor.submit(playMiniMax, depth, ShowMoves,copy.deepcopy(chess.Board())) for _ in range(NumberOfIterations)]
                results = [f.result() for f in concurrent.futures.as_completed(futures)]
        elif agent=="par":
            playpar(depth)
        else:

            print(" incorrect input Usage example: python MiniMax 3")
    except Exception as e:
        print(f"an error  has eccored{e}")




'''with open("game_output.pgn", "w") as pgn_file:
    print(game, file=pgn_file)
WritenewGeneratedMoves()'''

print("totalTime Taken",time.strftime("%H:%M:%S", time.localtime()))
