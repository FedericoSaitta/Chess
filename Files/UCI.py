import sys
from Board_state import get_all_valid_moves, generate_from_FEN, make_move
from Search import iterative_deepening


ranks_to_rows = {'1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0}
rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}  # To reverse the dictionary

files_to_cols = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
cols_to_files = {v: k for k, v in files_to_cols.items()}

promotion_pieces = {'q': 900, 'r': 500, 'b': 330, 'n': 320}

piece_dict = {100: 'p', 500: 'r', 330: 'b', 320: 'n', 900: 'q', None: None}

dict, board = generate_from_FEN()


THINKING_TIME = 2
engine_ID = 'id name Aquatic_Python'
author_ID = 'id author Federico Saitta'

'''IMPORTANT'''

def uci():
    print(engine_ID)
    print("uciok")

def is_ready():
    print("readyok")

def position(fen):
    global board, dict

    if fen != ['startpos']:
        previous_move = fen[-1]

        previous_start = files_to_cols[previous_move[0]] + int(previous_move[1]) * 8
        previous_end = files_to_cols[previous_move[2]] + int(previous_move[3]) * 8
        promotion_piece = None

        if len(previous_move) == 5:
            promotion_piece = promotion_pieces[previous_move[-1]]

        for move in get_all_valid_moves(board, dict):
            if (move.start_ind == previous_start) and (move.end_ind == previous_end):
                if move.prom_piece == promotion_piece:
                    make_move(board, move, dict)
                    break


def go(board, dict, Time):

    valid_moves = get_all_valid_moves(board, dict)
    move = iterative_deepening(valid_moves, board, dict, Time)

    move_notation = get_chess_notation((move.start_ind, move.end_ind), move.prom_piece)
    print(f"bestmove {move_notation}")

def get_chess_notation(tuple, prom_piece):
    start, end = tuple
    start_row, start_col = start // 8, start % 8
    end_row, end_col = end // 8, end % 8

    if prom_piece == None:
        first = cols_to_files[start_col] + rows_to_ranks[start_row]
        second = cols_to_files[end_col] + rows_to_ranks[end_row]
    else:
        piece = piece_dict[prom_piece]
        first = cols_to_files[start_col] + rows_to_ranks[start_row]
        second = cols_to_files[end_col] + rows_to_ranks[end_row] + piece

    return (first + second)

import asyncio
import sys

# ... (your existing code)

async def async_main():
    while True:
        # Read input command
        line = (await loop.run_in_executor(None, sys.stdin.readline)).strip()

        if 'uci' in line:
            uci()
        elif line == "isready":
            is_ready()
        elif line.startswith("position"):
            parts = line.split(" ")
            fen = parts[1:]
            position(fen)
        elif line.startswith("go"):
           go(board, dict, THINKING_TIME)
        elif line.startswith('exit'):
            break

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_main())

# You can make it start quicker probs by deleting some of those things that you dont need

# Make sure you are not in venv when building UCI though
# The line is: pyinstaller --onefile --add-data "Opening_repertoire.txt:." UCI.py
# python3 lichess-bot.py -u
