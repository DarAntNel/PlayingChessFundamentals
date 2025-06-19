import os
import asyncio
import chess
from groq import AsyncGroq
from IPython.display import SVG, display
import webbrowser
import chess.svg
import chess.syzygy
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
client = AsyncGroq(api_key=api_key)


SYSTEM_PROMPT = (
    "You're a chess engine. I will provide FENs of positions, legal moves and piece color move turn it starts with white. "
    "Respond with exactly one SAN move (e.g., 'Qh4#') and nothing else."
)


history = [{"role": "system", "content": SYSTEM_PROMPT}]

async def get_move_from_groq(board: chess.Board) -> str:
    fen = board.fen()
    legal_moves = board.legal_moves
    if board.turn == chess.WHITE:
        history.append({"role": "user", "content": f"Position FEN: {fen}, Turn : White, Legal Moves : {legal_moves} "})
    else:
        history.append({"role": "user", "content": f"Position FEN: {fen}, Turn : Black, Legal Moves : {legal_moves} "})

    resp = await client.chat.completions.create(
        model="llama3-8b-8192",
        messages=history
    )
    move_str = resp.choices[0].message.content.strip()
    history.append({"role": "assistant", "content": move_str})
    return move_str






async def play_full_game():
    board = chess.Board()
    print(board, "\n")

    while not board.is_game_over():
        move_str = await get_move_from_groq(board)
        print(move_str)
        print("LLM move:", move_str)

        try:
            move = board.parse_san(move_str)
            print(move)
            if move not in board.legal_moves:
                print("Illegal move:", move_str)
                break
        except Exception:
            print("Invalid SAN:", move_str)
            break

        board.push(move)

        with open("test.svg", "w") as f:
            f.write(chess.svg.board(board))
        webbrowser.open('file://' + os.path.realpath("test.svg"))

        if board.can_claim_threefold_repetition():
            print("Threefold repetition detected! Game can be ended as a draw.")
            break

    print("Game over:", board.result())

if __name__ == "__main__":
    asyncio.run(play_full_game())
