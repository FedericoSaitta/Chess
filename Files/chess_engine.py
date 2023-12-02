from math import fabs

'''CONSTANTS needed for look-ups'''

ranks_to_rows = {'1': 7, '2': 6, '3': 5, '4': 4,
                 '5': 3, '6': 2, '7': 1, '8': 0}
rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}  # To reverse the dictionary

files_to_cols = {'a': 0, 'b': 1, 'c': 2, 'd': 3,
                 'e': 4, 'f': 5, 'g': 6, 'h': 7}
cols_to_files = {v: k for k, v in files_to_cols.items()}

BISHOP_MOVES = ( (1, 1), (1, -1), (-1, 1), (-1, -1) )
ROOK_MOVES = ( (1, 0), (-1, 0), (0, 1), (0, -1) )

KING_MOVES = ( (1, 0), (-1, 0), (0, 1), (0, -1),  # These are moves that look forwards
                  (-1, -1), (1, -1), (1, 1), (-1, 1) )   # These look diagonally

KNIGHT_MOVES = ( (2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2) )


QUEEN_MOVES = ( (1, 1), (1, -1), (-1, 1), (-1, -1),  # Diagonal
                   (1, 0), (-1, 0), (0, 1), (0, -1) )  # Perpendicular

WHITE_PAWN_MOVES = ( (-1, 0), (- 1, -1), (-1, 1) )

BLACK_PAWN_MOVES = ( (1, 0), (1, -1), (1, 1) )


WHITE_CASTLE_SQ = ( (-1, -1, {300, 900}), (-1, 1, {300, 900}), (-1, 0, {500, 900}), # Diagonal and vertical moves
                    (-1, -2), (-1, 2), (-2, -1), (-2, 1) )  # Knight moves

BLACK_CASTLE_SQ = ( (1, -1, {300, 900}), (1, 1, {300, 900}), (1, 0, {500, 900}), # Diagonal and vertical moves
                    (1, -2), (1, 2), (2, -1), (2, 1) )  # Knight moves



'''Here are the variables that will be re-assigned and changed during run time'''

board = [  # Switching to a 1D board representation    # Left right is +/- 1 and up and down is +/- 8
    -500, -293, -300, -900,   -1, -300, -293, -500,  # 0 to 7
    -100, -100, -100, -100, -100, -100, -100, -100,  # 8 to 15
      0 ,   0 ,   0 ,   0 ,   0 ,   0 ,   0 ,   0 ,  # 16 to 23
      0 ,   0 ,   0 ,   0 ,   0 ,   0 ,   0 ,   0 ,  # 24 to 31
      0 ,   0 ,   0 ,   0 ,   0 ,   0 ,   0 ,   0 ,  # 32 to 39
      0 ,   0 ,   0 ,   0 ,   0 ,   0 ,   0 ,   0 ,  # 40 to 47
     100,  100,  100,  100,  100,  100,  100,  100,  # 48 to 55
     500,  293,  300,  900,   1 ,  300,  293,  500]  # 56 to 63

# Dictionary with kwargs needed during a game
general_dict = {'white_to_move': True,
                'white_king_loc': 60,
                'black_king_loc': 4,
                'white_en_passant_sq': None,
                'black_en_passant_sq': None,
                'check_mate': False,
                'stale_mate': False,
                'move_log': [],
                'white_castle': [True, True],  #  [Left, Right]
                'black_castle': [True, True], # These simply state whether the right is still there, not if the move
                'castle_rights_log': []  # [left, right], even means white, odd means black, each turn a tuple of two
                                                           # values is added
}

def make_move(board, move, dict):

    if move.piece_moved == 1:
        dict['white_king_loc'] = move.end_ind
    elif move.piece_moved == -1:
        dict['black_king_loc'] = move.end_ind

    '''Checks for possibility of enpassant'''
    if move.piece_moved == 100 or move.piece_moved == -100:
        if move.start_ind // 8 == 1 and move.end_ind // 8 == 3:
            dict['black_en_passant_sq'] = move.end_ind - 8
        elif move.start_ind // 8 == 6 and move.end_ind // 8 == 4:
            dict['white_en_passant_sq'] = move.end_ind + 8

    '''Checks if castling rights should be removed'''
    if fabs(move.piece_moved) == 500 or fabs(move.piece_moved) == 1 or fabs(move.piece_captured) == 500:
        if move.piece_moved == 1:
            dict['white_castle']= [False, False]
        elif move.piece_moved == 500:
            if move.start_ind == 63:
                dict['white_castle'][1] = False
            else:
                dict['white_castle'][0] = False

        elif move.piece_moved == -1:
            dict['black_castle'] = [False, False]

        elif move.piece_moved == -500:
            if move.start_ind == 7:
                dict['black_castle'][1] = False
            else:
                dict['black_castle'][0] = False

        if move.piece_captured == 500:
            if move.end_ind == 63:
                dict['white_castle'][1] = False
            else:
                dict['white_castle'][0] = False

        elif move.piece_captured == -500:
            if move.end_ind == 7:
                dict['black_castle'][1] = False
            else:
                dict['black_castle'][0] = False

    '''If the move is an en-passant'''
    if move.en_passant:
        if move.piece_moved > 0:
            board[move.end_ind + 8] = 0
        else:
            board[move.end_ind - 8] = 0

    '''If the move is a castling move'''
    if move.castle_move:
        if move.piece_moved > 0:
            if move.end_ind == 62:  # Right castle
                board[63], board[61] = 0, 500
            else:
                board[56], board[59] = 0, 500

        else:
            if move.end_ind == 6: # Right castle
                board[7], board[5] = 0, -500
            else:
                board[0], board[3] = 0, -500

    board[move.start_ind], board[move.end_ind] = 0, move.piece_moved
    dict['move_log'].append(move)
    dict['white_to_move'] = not dict['white_to_move']  # Swap the player's move

    tup = (dict['white_castle'], dict['black_castle'])
    dict['castle_rights_log'].append(tup)

    return board, dict

def undo_move(board, dict): # This method doesn't need to be super efficient as it should not be used anyway, unless the
                            # player needs to, engine should not use it to see for checks
    if len(dict['move_log']) > 0:
        move = dict['move_log'].pop()
        if move.en_passant:
            if dict['white_to_move']: # Means that white made an en-passant move
                board[move.end_ind - 8], dict['white_en_passant_sq'] = 100, move.end_ind
            else:
                board[move.end_ind + 8], dict['black_en_passant_sq'] = -100, move.end_ind

        board[move.start_ind], board[move.end_ind] = move.piece_moved, move.piece_captured
        dict['white_to_move'] = not dict['white_to_move']

        '''Bring back rooks if the last move was a castling move'''
        if move.castle_move:
            if move.end_ind == 62: board[61], board[63] = 0, 500
            elif move.end_ind == 59: board[59], board[56] = 0, 500
            elif move.end_ind == 6: board[5], board[7] = 0, -500
            else: board[3], board[0] = 0, -500

        '''Need to give back the previous castling rights'''
        dict['white_castle'] = dict['castle_rights_log'][-1][0]
        dict['black_castle'] = dict['castle_rights_log'][-1][1]

        '''Keeping track of the kings locations'''
        if move.piece_moved == 1: dict['white_king_loc'] = move.start_ind
        elif move.piece_moved == -1: dict['black_king_loc'] = (move.start_ind)

    return board, dict

'''Used to determine whether castling squares are under attack only'''
def un_attacked_sq(board, ind, row, col, dict, king_color):  # Determine if the enemy can attack the square (r, c), used to determine validity of castling only
    # Should check if diagonally one space away there is a king, and diagonally queen and bishop and vertically and horizontally
    # if there is a queen or a rook, do pawns separately, should also check knights separately

    # As this only needs to check very few possible configurations there is no need to run a full checking search
    if king_color: # Means that it is a white king
        MOVES = WHITE_CASTLE_SQ
    else:
        MOVES = BLACK_CASTLE_SQ

# There are some problems with this function
    for index, tup in enumerate(MOVES):
        if index < 3:  # Diagonals
            square = 8 * (row + tup[0]) + tup[1] + col
            if ((board[square] > 0) != king_color) and board[square] != 0: # Checks for colour
                piece = fabs(board[square])
                if piece in tup[2] or (index < 2 and (piece == 100 or piece == 1)):
                    return False                                   # So that side cannot castle
            elif board[square] != 0:
                continue # As there is a piece of your own colour
            else: # We need to keep looking ahead
                for mul in range(2, 8):
                    if -1 < (row + (mul * tup[0])) < 8 and -1 < (col + (mul * tup[1])) < 8:
                        square = 8 * (row + mul * tup[0]) + (col + mul * tup[1])
                        if ((board[square] > 0) != king_color) and board[square] != 0:
                            piece = fabs(board[square])
                            if piece in tup[2]:
                                return False
                            else:
                                break  # We need to break out as enemy piece that cant capture is blocking
                        elif board[square] == 0:
                            continue
                        else:
                            break
                    else:
                        break
        else:  # Knight moves
            square = 8 * (row + tup[0]) + tup[1] + col
            if ((board[square] > 0) != king_color) and board[square] != 0:  # Checks for colour
                piece = fabs(board[square])
                if piece == 293:
                    return False  # So that side cannot castle
    return True

def in_check(board, dict):
    if dict['white_to_move']:
        return un_attacked_sq(board, dict['white_king_loc'])
    else:
        return un_attacked_sq(board, dict['black_king_loc'])

def get_P_moves(moves, board, ind, row, col, dict, MOVES):
    for index, tup in enumerate(MOVES):
        if -1 < (row + tup[0]) < 8 and -1 < (col + tup[1]) < 8:
            square = 8 * (row + tup[0])  + tup[1] + col

            if index == 0:
                if board[square] == 0:
                    moves.append(Move(ind, square, board))

                    if row == 1 and board[ind] < 0:  # Checking for double move
                        square += 8                  # Goes forth one row
                        if board[square] == 0:
                            moves.append(Move(ind, square, board))

                    elif row == 6 and board[ind] > 0:
                        square -= 8                   # Goes back one row
                        if board[square] == 0:
                            moves.append(Move(ind, square, board))
            else:
                if ((board[square] > 0) != (board[ind] > 0)) and board[square] != 0:
                    moves.append(Move(ind, square, board))

                elif board[ind] > 0 and (square == dict['black_en_passant_sq']):
                    moves.append(Move(ind, square, board, (False, True)))   # tup is (castle, en_passant) identifier

                elif board[ind] < 0 and (square == dict['white_en_passant_sq']):    # As the piece is definetely black
                    moves.append(Move(ind, square, board, (False, True)))

def get_Sliding_moves(moves, board, ind, row, col, MOVES):
    for tup in MOVES:
        if -1 < (row + tup[0]) < 8 and -1 < (col + tup[1]) < 8:
            square = 8 * (row + tup[0]) + (col + tup[1])
            if (board[square] != 0) and  ((board[square] >= 0) == (board[ind] > 0)):
                continue

            elif board[square] != 0:
                    moves.append(Move(ind, square, board))
                    continue  # Means that it is an enemy piece
            else:

                moves.append(Move(ind, square, board))

                for mul in range(2, 8):
                    if -1 < (row + (mul * tup[0])) < 8 and -1 < (col + (mul * tup[1])) < 8:
                        square = 8 * (row + mul * tup[0]) + (col + mul * tup[1])
                        if (board[square] != 0) and (board[square] > 0) == (board[ind] > 0):
                            break
                        elif board[square] != 0:  # Means that it is an enemy piece
                            moves.append(Move(ind, square, board))
                            break
                        else:
                            moves.append(Move(ind, square, board))
                    else:
                        break

def get_N_moves(moves, board, ind, row, col):
    for tup in KNIGHT_MOVES:
        if -1 < (row + tup[0]) < 8 and -1 < (col + tup[1]) < 8:
            square = 8 * (row + tup[0]) + (col + tup[1])
            if (board[square] == 0) or (board[square] >  0) != (board[ind] > 0):
                    moves.append(Move(ind, square, board))

def get_K_moves(moves, board, ind, row, col, dict):
    for tup in KING_MOVES:
        if -1 < (row + tup[0]) < 8 and -1 < (col + tup[1]) < 8:
            square = 8 * (row + tup[0]) + (col + tup[1])
            if (board[square] == 0) or ((board[square] >  0) != (board[ind] > 0)):
                moves.append(Move(ind, square, board))

    # Now checking for castling
    if dict['white_to_move']:
        if dict['white_castle'][1]:
            if board[61] == 0 and board[62] == 0:
                if (un_attacked_sq(board, 61, 7, 5, dict, True)) and (un_attacked_sq(board, 62, 7, 6, dict, True)):
                    moves.append(Move(ind, 62, board, (True, False)))

        if dict['white_castle'][0]:
            if board[59] == 0 and board[58] == 0:
                if (un_attacked_sq(board, 59, 7, 3, dict, True)) and (un_attacked_sq(board, 58, 7, 2, dict, True)):
                    moves.append(Move(ind, 58, board, (True, False)))
    else:
        if dict['black_castle'][1]:
            if board[5] == 0 and board[6] == 0:
                if (un_attacked_sq(board, 5, 0, 5, dict, False)) and (un_attacked_sq(board, 6, 0, 6, dict, False)):
                    moves.append(Move(ind, 6, board, (True, False)))
        if dict['black_castle'][0]:
            if board[3] == 0 and board[2] == 0:
                if (un_attacked_sq(board, 3, 0, 3, dict, False)) and (un_attacked_sq(board, 2, 0, 2, dict, False)):
                    moves.append(Move(ind, 2, board, (True, False)))

def get_all_possible_moves(board, dict): # Using all these if statements as it is fastest
    moves = []

    for ind in range(64):
        col, row = ind % 8, ind // 8
        if board[ind] == 0: continue

        if (board[ind] > 0 and dict['white_to_move']) or (board[ind] < 0 and not dict['white_to_move']):
            piece = fabs(board[ind])

            if piece == 100:
                if board[ind] > 0:
                    get_P_moves(moves, board, ind, row, col, dict, WHITE_PAWN_MOVES)
                else:
                    get_P_moves(moves, board, ind, row, col, dict, BLACK_PAWN_MOVES)

            elif piece == 500: get_Sliding_moves(moves, board, ind, row, col, ROOK_MOVES)
            elif piece == 293: get_N_moves(moves, board, ind, row, col)
            elif piece == 300: get_Sliding_moves(moves, board, ind, row, col, BISHOP_MOVES)
            elif piece == 900: get_Sliding_moves(moves, board, ind, row, col, QUEEN_MOVES)
            elif piece == 1: get_K_moves(moves, board, ind, row, col, dict)

    return moves

def get_all_valid_moves(board, dict):  # This will take into account non-legal moves that put our king in check

    moves = get_all_possible_moves(board, dict)
    '''
    for i in range(len(moves) - 1, -1, -1):  # Going backwards through loop
        board = make_move(board, moves[i])
        white_to_move = not white_to_move

        if in_check(board):
            moves.remove(moves[i])

        white_to_move = not white_to_move
        board = undo_move(board)

        if len(moves) == 0:
            if in_check():
                print(f'Check Mate on the Board, white wins: {not white_to_move}')
                check_mate = True
            else:
                print(f'We have a Stale Mate on the board, none wins')
                stale_mate = True
        else:
            check_mate, stale_mate = False, False
        '''
    return moves

class Move:

    __slots__ = ('start_ind', 'end_ind', 'move_ID',
                 'piece_moved', 'piece_captured', 'castle_move', 'en_passant')


    def __init__(self, start_sq, end_sq, board, tup = (False, False)):

        self.start_ind, self.end_ind = start_sq, end_sq

        self.piece_moved = board[self.start_ind]
        self.piece_captured = board[self.end_ind]
        self.castle_move, self.en_passant = tup

        # Similar idea to hash function
        self.move_ID = self.start_ind * 100 + self.end_ind


    def get_chess_notation(self, board):
        dict = {-100: 'bP', 100: 'wP', -500: 'bR', 500: 'wR', -300: 'bB', 300: 'wB',
                -293: 'bN', 293: 'wN', -900: 'bQ', 900: 'wQ', -1: 'bK', 1: 'wK'}

        piece = board[self.start_ind]
        start_rank_file = self.get_rank_file(self.start_ind)
        end_rank_file = self.get_rank_file(self.end_ind)

        if fabs(piece) == 100:
            if board[self.end_ind] != 0:
                return dict[piece][1:] + start_rank_file + ' x ' + end_rank_file

        if board[self.end_ind] != 0:
            return dict[piece][1:] + start_rank_file + ' x ' + end_rank_file

        return dict[piece][1:] + start_rank_file + ' to ' + end_rank_file

    def get_rank_file(self, index):
        c = index % 8
        r = index // 8
        return cols_to_files[c] + rows_to_ranks[r]

    def __eq__(self, other):  # Note the other move is the one stored in the valid_moves list
        if isinstance(other, Move):
            if (self.move_ID == other.move_ID) and other.castle_move:
                self.castle_move = True
                return True
            elif (self.move_ID == other.move_ID) and other.en_passant:
                self.en_passant = True
                return True

            elif (self.move_ID == other.move_ID):
                return True
        return False