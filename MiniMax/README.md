# Evaluation Function Progress
🟢 Completed
🔴 Not Started
🟡 In Progress
## 1. Items  to consider during evaluation



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

- #### Number of Major pieces, Minor pieces, and pawns🔴
       the less pieces  you have the less attacks you can make and the less
       squares you can control.  reduce the evaluation by  the total value of
       of loss pieces*2

- #### distant from king 🔴
       each piece moves differently if a move increases  the mobility of then
       opponent king reduce its value
       if it reduces it increase the value of the piece by the total value of
       all your pieces on the board

- #### pawn rank🟢
       pawn rank is assigned  based on how far you are for you  form the home square


- #### piece(not pawns) rank( relative to  opponents king)🔴
      piece rank is increased the closer it gets to the opponent king and is
      based on the type of piece and how many moves it will take to check the opponent
      king
- #### blank spaces 🔴
- #### reduced  king mobility 🔴
- #### unprotected king 🔴
- #### center control 🔴
- #### Attacked  and defended 🟡
       this is almost finished for white
## 2. Evaluation Speed
- #### Parallelism 🔴
       By dividing the number of legal move between the number of processors
       some amount of speed can be achieved.  The current implementation is only
       able to go 3 move ahead(ie., whitte->black->white 1.5 if we count white
       and black as 1),  this evaluates to approximately  10 seconds per play.
       when it  it increase to 4(white,black,white,black)
