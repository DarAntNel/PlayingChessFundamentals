# Evaluation Function Progress
🟢 Completed
🔴 Not Started
🟡 In Progress
## 1. Items  to consider during evaluation
### code execution:
- install Stockfish on  you local machine a and change the path on line 16 of MiniMax.py
- run command python -m http.server 8000
- to see gameplay without opening new window visit http://localhost:8000/PLayEngine.html
- run python PLayEngine.py MiniMax 3 /// this number cannot be incereased else you will think the system is broke
you can try with the value 1. 2 will  not work as there is not evaluation for  white(i.e the function will always return 0  and will play very badly)



- #### Piece Capture 🟡
       if the last move is a capture increase the evaluation value by the total
       value of the piece that was captured +  the rank the piece is on. if its
       a pawn rank=distance from home square
       if its a piece   rank is relative to king. this also considers the piece
       type and how many move to get to opponent king
- #### King is in check 🔴
       if your king is in check and  the piece checking you king is not attacked
       (you must move your king) therefore you evaluation becomes 0
       if  you are checking the opponent king  and your pieces is not attacked
       increase you piece current value by itself

- #### Number of Major pieces, Minor pieces, and pawns 🟡
       the less pieces  you have the less attacks you can make and the less
       squares you can control.  reduce the evaluation by  the total value of
       of loss

- #### distant from king 🔴
       each piece moves differently if a move increases  the mobility of then
       opponent king reduce its value
       if it reduces it increase the value of the piece by the total value of
       all your pieces on the board
- #### controled spaces colosest to king

- #### pawn rank🟡 # this just a few more adjustments needed here
       pawn rank is assigned  based on how far you are for you  form the home square
  #### Piece Rank 🟡
- #### piece(not pawns) rank( relative to  opponents king)🟡
      piece rank is increased the closer it gets to the opponent king and is
      based on the type of piece and how many moves it will take to check the opponent
      king
- #### blank spaces 🟡
       the evaluation of blank spaces  has been partially implemented
- #### reduced  king mobility 🔴
- #### unprotected king 🔴
- #### center control 🟡
- #### Attacked  and defended 🟡
       this is almost finished for white
## 2. Evaluation Speed
- #### Parallelism 🔴 # attempted but not working
       By dividing the number of legal move between the number of processors
       some amount of speed can be achieved.  The current implementation is only
       able to go 3 move ahead(ie., whitte->black->white 1.5 if we count white
       and black as 1),  this evaluates to approximately  10 seconds per play.
       when it  it increase to 4(white,black,white,black)
       -----------------------------------------------------------------------
       The Parallelism implements takes longer than the serial execuction
