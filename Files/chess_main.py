# Handling user input and displaying the current GameState object
import pygame as p
from Files import chess_engine


WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = WIDTH/DIMENSION
MAX_FPS = 10# comes into play when animating images
IMAGES = {}

def load_images():
    path = '/Users/federicosaitta/PycharmProjects/Chess/Images/'
    pieces = ['wP', 'bP', 'wR', 'bR', 'wN', 'bN', 'wB', 'bB', 'wQ', 'bQ', 'wK', 'bK']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(path + piece + '.png'), (SQ_SIZE, SQ_SIZE))

# Handle user input and update graphics
def main(): # Standard game loop for a game
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color('white'))
    gs = chess_engine.GameState()
    valid_moves = gs.get_all_possible_moves()

    move_made = False # Flag for when we want to generate this function

    load_images() # important to do this only once (expensive process)

    running = True
    sq_selected = () # keep track of last input from user
    player_clicks = [] # keep track of player clicks, two tuples

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            # Mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:  # Change this to add dragging pieces
                location = p.mouse.get_pos()  # Note if you add extra panels note to keep track of those
                col = int(location[0]//SQ_SIZE)
                row = int(location[1]//SQ_SIZE)


                if sq_selected == (row, col):
                    sq_selected = () # deselects if player clicks twice
                    player_clicks = []

                else:
                    sq_selected = (row, col)
                    player_clicks.append(sq_selected)  # Append both first and second clicks

                if len(player_clicks) == 2:

                    move = chess_engine.Move(player_clicks[0], player_clicks[1], gs.board)

                    if move in valid_moves:
                        gs.make_move(move)
                        move_made = True

                    sq_selected = ()
                    player_clicks = []

            # Key press handler

            elif e.type == p.KEYDOWN:
                '''if e.key == p.K_z: # Do not allow for undo moves for now
                    gs.undo_move()
                    move_made = True
                '''

                if e.key == p.K_LEFT: # Use these to go through previous moves
                    pass

                elif e.key == p.K_RIGHT:
                    pass

        if move_made:
            valid_moves = gs.get_all_possible_moves() # Note this will need to be valid moves only in the future
            move_made = False

        draw_game_state(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

# Responsible for all the graphics
def draw_game_state(screen, gs):  # Drawing is done once per frame
    draw_board(screen)
    # Use this method later to add piece highlighting and move suggestions etc
    draw_pieces(screen, gs.board)


def draw_board(screen): # Draws the squares on the board
    colors = [p.Color((238,238,210)), p.Color((118,160,86))]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

# we keep these separate if we want to high squares, highlighting under piece above square

def draw_pieces(screen, board): # Draws the pieces, need to draw them after the board
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != '--':

               screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == '__main__':
    main()