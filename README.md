# PlayingChessFundamentals
PlayingChessFundamentals


In this project we make use of the python-chess project to simulate
chess gameplay using our newly implemented search and decision making algorithms
gameplay is done running "python gameplay.py"
Directories containing our code include:
LLM, MiniMax, Expectimax, Alphabeta, Evaluation.
Stockfish engine is located in folder stockfish.
Please note when running the gameplay.py, you will need to add a .env file to this project in your local repository containing an API key to groc.
The .pgn files in the root directory contains the history of some games played from the gameplay.py.
You should be able to copy games into online engines and see moves played. 


The following is an example of a single game recorded, these files contain multiple games appended all in one file.

[Event "expectimax_vs_stockfish"]
[Site "?"]
[Date "????.??.??"]
[Round "?"]
[White "Stockfish UCI_Elo 1320"]
[Black "Expectimax"]
[Result "*"]
[FEN "1k6/2R1N3/3K4/8/8/8/8/8 w - - 0 1"]
[SetUp "1"]

1. Rc4 Ka7 2. Rc5 Kb6 3. Rh5 Kb7 4. Nf5 Kb8 5. Kc6 Ka7 6. Nh4 Kb8 7. Ng6 Ka7 8. Kc7 Ka6 9. Kc8 Ka7 10. Kd8 Kb7 11. Rh1 Ka7 12. Rh6 Kb7 13. Nf8 Ka7 14. Kc7 *
