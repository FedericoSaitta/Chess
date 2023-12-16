# Evaluates positions and searches moves
import chess_engine
from random import randint
from math import fabs
import timeit

# If when we score the board, positive values indicate white is winning
FABS = fabs
CHECK_MATE = 100_000
STALE_MATE = 0

PAWN_white = (0,  0,  0,  0,  0,  0,  0,  0,
          50, 50, 50, 50, 50, 50, 50, 50,
          10, 10, 20, 30, 30, 20, 10, 10,
           5,  5, 10, 25, 25, 10,  5,  5,
           0,  0,  0, 20, 20,  0,  0,  0,
           5, -5,-10,  0,  0,-10, -5,  5,
           5, 10, 10,-20,-20, 10, 10,  5,
           0,  0,  0,  0,  0,  0,  0,  0)

KNIGHT_white = ( -50,-40,-30,-30,-30,-30,-40,-50,
           -40,-20,  0,  0,  0,  0,-20,-40,
           -30,  0, 10, 15, 15, 10,  0,-30,
           -30,  5, 15, 20, 20, 15,  5,-30,
           -30,  0, 15, 20, 20, 15,  0,-30,
           -30,  5, 10, 15, 15, 10,  5,-30,
           -40,-20,  0,  5,  5,  0,-20,-40,
           -50,-40,-30,-30,-30,-30,-40,-50)

BISHOP_white = ( -20,-10,-10,-10,-10,-10,-10,-20,
            -10,  0,  0,  0,  0,  0,  0,-10,
            -10,  0,  5, 10, 10,  5,  0,-10,
            -10,  5,  5, 10, 10,  5,  5,-10,
            -10,  0, 10, 10, 10, 10,  0,-10,
            -10, 10, 10, 10, 10, 10, 10,-10,
            -10,  5,  0,  0,  0,  0,  5,-10,
            -20,-10,-10,-10,-10,-10,-10,-20)

ROOK_white = ( 0,  0,  0,  0,  0,  0,  0,  0,
              5, 10, 10, 10, 10, 10, 10,  5,
             -5,  0,  0,  0,  0,  0,  0, -5,
             -5,  0,  0,  0,  0,  0,  0, -5,
             -5,  0,  0,  0,  0,  0,  0, -5,
             -5,  0,  0,  0,  0,  0,  0, -5,
             -5,  0,  0,  0,  0,  0,  0, -5,
              0,  0,  0,  5,  5,  0,  0,  0)

QUEEN_white = (-20,-10,-10, -5, -5,-10,-10,-20,
                -10,  0,  0,  0,  0,  0,  0,-10,
                -10,  0,  5,  5,  5,  5,  0,-10,
                 -5,  0,  5,  5,  5,  5,  0, -5,
                  0,  0,  5,  5,  5,  5,  0, -5,
                -10,  5,  5,  5,  5,  5,  0,-10,
                -10,  0,  5,  0,  0,  0,  0,-10,
                -20,-10,-10, -5, -5,-10,-10,-20)

KING_white = (-30,-40,-40,-50,-50,-40,-40,-30,
            -30,-40,-40,-50,-50,-40,-40,-30,
            -30,-40,-40,-50,-50,-40,-40,-30,
            -30,-40,-40,-50,-50,-40,-40,-30,
            -20,-30,-30,-40,-40,-30,-30,-20,
            -10,-20,-20,-20,-20,-20,-20,-10,
             20, 20,  0,  0,  0,  0, 20, 20,
             20, 30, 10,  0,  0, 10, 30, 20)

'''         (20, 30, 10, 0, 0, 10, 30, 20, 
             20, 20, 0, 0, 0, 0, 20, 20, 
            -10, -20, -20, -20, -20, -20, -20, -10, 
            -20, -30, -30, -40, -40, -30, -30, -20, 
            -30, -40, -40, -50, -50, -40, -40, -30, 
            -30, -40, -40, -50, -50, -40, -40, -30, 
            -30, -40, -40, -50, -50, -40, -40, -30, 
            -30, -40, -40, -50, -50, -40, -40, -30)
            
'''


PAWN_black = tuple(reversed(PAWN_white))

print(PAWN_black)


KNIGHT_black = tuple(reversed(KNIGHT_white))
BISHOP_black = tuple(reversed(BISHOP_white))
ROOK_black = tuple(reversed(ROOK_white))
QUEEN_black  = tuple(reversed(QUEEN_white))
KING_black = tuple(reversed(KING_white))
print(KING_black)

piece_sq_values = {100: PAWN_white, -100:PAWN_black,
                   293: KNIGHT_white, -293: KNIGHT_black,
                   300: BISHOP_white, -300: BISHOP_black,
                   500: ROOK_white, -500: ROOK_black,
                   900: QUEEN_white, -900: QUEEN_black,
                   1: KING_white, -1: KING_black}

def find_random_move(moves):
    if moves != []:
        index = randint(0, len(moves) - 1)
        return moves[index]
    else:
        return None


def best_move_finder(moves, board, dict):
    ### From this alg perspective both black and white aim for high scores, this is maximizing algorithm
    turn_multiplier = -1 if dict['white_to_move'] else 1
    max_score = - CHECK_MATE
    best_move = None

    for move in moves:
        print(move.get_chess_notation(board))
        chess_engine.make_move(board, move, dict)
        score = evaluate_board(board, dict) * turn_multiplier
        chess_engine.undo_move(board, dict)
        print(score, max_score)
        if score > max_score:
            max_score = score
            best_move = move

    print('eval_bar: ', max_score)
    return best_move


def evaluate_board(board, dict):
    ## Putting the dict here for now, will change later probs
    # For now this is just a rudimentary method
    if dict['check_mate']: return CHECK_MATE
    elif dict['stale_mate']: return STALE_MATE

    else:
        eval_bar = 0
        index = 0
        for square in board:
            if square != 0:
                eval_bar += (piece_sq_values[square])[index]

            index += 1

        eval_bar += sum(board)

        return eval_bar/100