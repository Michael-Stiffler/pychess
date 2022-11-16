import pygame as py
import os
import math

#constants. SIZE is pixel LENGTH of each square on the board and LENGTH is how many squares per column or row.
IMAGES = {}
LENGTH = 8
SIZE = 100
        
#colors for black and white squares as well as the highlight color
whiteColor = (255, 255, 255, 255)
blackColor =  (205, 129, 70, 255)
highlight_color = (101, 67, 45, 140)
        
piece_held = None
current_user_square = None
board = [[None for i in range(LENGTH)] for j in range(LENGTH)]

#set a pygame surface object for a square on the board with alpha and keep that square
square_surface = py.Surface((100,100), py.SRCALPHA)      
square_surface_rect = square_surface.get_rect(topleft=(0,0))
        
def draw_board(display):
        count = 0
        for x in range(1, LENGTH + 1):
            for y in range(1, LENGTH + 1):
                if count % 2 == 0:
                    py.draw.rect(display, whiteColor, [
                                SIZE*y - SIZE, SIZE*x - SIZE, SIZE, SIZE])
                else:
                    py.draw.rect(display, blackColor,[
                                SIZE*y - SIZE, SIZE*x - SIZE, SIZE, SIZE])
                count += 1
            count -= 1
                        
def load_pieces():
        pieces = ['bB', 'bK', 'bN', 'bP', 'bQ',
                 'bR', 'wB', 'wK', 'wN', 'wP', 'wQ', 'wR']
        for piece in pieces:
            source_file_dir = os.path.dirname(os.path.abspath(os.getcwd()))
            image_path = os.path.join(source_file_dir, "pychess\\piece_images\\" + piece + '.png')
            IMAGES[piece] = py.transform.scale(py.image.load(image_path), (SIZE, SIZE))
            
def draw_pieces(_board, display):
    board = _board
    for x in range(LENGTH):
            for y in range(LENGTH):
                piece = board[x][y]
                if piece:
                    display.blit(IMAGES[piece.filename], py.Rect(piece.x*SIZE, piece.y*SIZE, SIZE, SIZE))
                    
def drag_piece(mouse_pos, _board, display):
    board = _board
    for x in range(LENGTH):
        for y in range(LENGTH):
            piece = board[x][y]
            if piece == piece_held:
                continue
            elif piece:
                display.blit(IMAGES[piece.filename], py.Rect(piece.x*SIZE, piece.y*SIZE, SIZE, SIZE))
    display.blit(IMAGES[piece_held.filename], (mouse_pos[0] - 50, mouse_pos[1] - 50))
        
def draw_moves(self, display):
    moves = self.piece_held.moves_no_algebraic_notation
    for move in moves:
        py.draw.circle(display, highlight_color, [
                                SIZE*(move[0] + 1) - (SIZE / 2), SIZE*(move[1] + 1) - (SIZE / 2)], 25)
            
def initialize_show_square(display):
    py.draw.rect(square_surface, highlight_color, square_surface_rect)
    display.blit(square_surface, square_surface_rect) 
        
def show_square(mouse_position, display):
    # this is for debugging purposes
        
    #formatted user position. ie (0,1), (2,2), etc
    square_postion_x, square_position_y = (math.floor(mouse_position[0] / SIZE), math.floor(mouse_position[1] / SIZE))
        
    #we want to check if the square the user is currently at is different than the last. 
    #helps not run through this process
    if current_user_square is None or current_user_square[0] != square_postion_x or current_user_square[1] != square_position_y:
            
        #draw the pieces and the board over what we have so it can reset each iteration
        draw_board()
        draw_pieces(board)
            
        #set the current_user_square to the one we just moved to
        current_user_square = (square_postion_x, square_position_y)
        #find and create the area around where the rectangle should be. ie (100,100), (300,400), etc.
        rect = (SIZE*(square_postion_x + 1) - SIZE, SIZE*(square_position_y + 1) - SIZE, SIZE, SIZE)
            
        #change the current topleft of that rectange to those new values. draw that rectange with a color. blit it on screen.
        square_surface_rect.topleft = (rect[0], rect[1])
        display.blit(square_surface, square_surface_rect) 
