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
    "You're a chess engine. I will provide FENs of positions,and piece color move turn it starts with white. "
    "Respond with exactly one SAN move (e.g., 'Qh4#') and nothing else."
)


history = [{"role": "system", "content": SYSTEM_PROMPT}]

async def get_move_from_groq(board: chess.Board) -> str:
    fen = board.fen()
    legal_moves = board.legal_moves
    if board.turn == chess.WHITE:
        history.append({"role": "user", "content": f"Position FEN: {fen}, Turn : White, "})
    else:
        history.append({"role": "user", "content": f"Position FEN: {fen}, Turn : Black, "})

    resp = await client.chat.completions.create(
        model="llama3-8b-8192",
        messages=history
    )
    move_str = resp.choices[0].message.content.strip()
    history.append({"role": "assistant", "content": move_str})

    return move_str







