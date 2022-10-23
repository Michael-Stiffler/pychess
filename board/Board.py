from re import S
import pygame as py
import math

class Board():
    
    def __init__(self, display, fen):
        self.display = display
        self.parse_fen(fen)
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
            ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
            ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
            ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        #self.board = None * 64
        self.size = 100
        self.length = 8
        self.whiteColor = (255, 255, 255, 255)
        self.blackColor =  (205, 129, 70, 255)
        self.highlight_color = (101, 67, 45, 140)
        self.IMAGES = {}
        self.current_user_square = None
        self.square_surface = py.Surface((100,100), py.SRCALPHA)      
        self.square_surface_rect = self.square_surface.get_rect(topleft=(0,0))
        self.white_to_move = True
        self.en_passant_target_square = ""
    
    def draw_board(self):
    
        count = 0
        for x in range(1, self.length + 1):
            for y in range(1, self.length + 1):
                if count % 2 == 0:
                    py.draw.rect(self.display, self.whiteColor, [
                                self.size*y - self.size, self.size*x - self.size, self.size, self.size])
                else:
                    py.draw.rect(self.display, self.blackColor, [
                                self.size*y - self.size, self.size*x - self.size, self.size, self.size])
                count += 1
            count -= 1
                        
    def load_pieces(self):
        pieces = ['bB', 'bK', 'bN', 'bP', 'bQ',
                'bR', 'wB', 'wK', 'wN', 'wP', 'wQ', 'wR']
        for piece in pieces:
            self.IMAGES[piece] = py.transform.scale(
                py.image.load("../piece-images/" + piece + ".png"), (self.size, self.size))
            
    def draw_pieces(self):
        for x in range(self.length):
            for y in range(self.length):
                piece = self.board[x][y]
                if len(piece.strip()) != 0:
                    self.display.blit(self.IMAGES[piece], py.Rect(y*self.size, x*self.size, self.size, self.size))
                    
    def show_square(self, mouse_position):
        # this is for debugging purposes
        
        #formatted user position. ie (0,1), (2,2), etc
        square_postion_x, square_position_y = (math.floor(mouse_position[0] / self.size), math.floor(mouse_position[1] / self.size))
        
        #we want to check if the square the user is currently at is different than the last. 
        #helps not run through this process
        if self.current_user_square is None or self.current_user_square[0] != square_postion_x or self.current_user_square[1] != square_position_y:
            
            #draw the pieces and the board over what we have so it can reset each iteration
            self.draw_board()
            self.draw_pieces()
            
            #set the current_user_square to the one we just moved to
            self.current_user_square = (square_postion_x, square_position_y)
            #find and create the area around where the rectangle should be. ie (100,100), (300,400), etc.
            rect = (self.size*(square_postion_x + 1) - self.size, self.size*(square_position_y + 1) - self.size, self.size, self.size)
            
            #change the current topleft of that rectange to those new values. draw that rectange with a color. blit it on screen.
            self.square_surface_rect.topleft = (rect[0], rect[1])
            self.display.blit(self.square_surface, self.square_surface_rect)  
            
    def initialize_show_square(self):
        py.draw.rect(self.square_surface, self.highlight_color, self.square_surface_rect)
        self.display.blit(self.square_surface, self.square_surface_rect)        
        
    def parse_fen(self, fen):
        # parse fen from this -> rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
        # to this -> ['rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR', 'w', 'KQkq', '-', '0', '1']
        #rn1q1rk1/ppp2ppp/4pn2/3p4/1b1P4/N1N1P1P1/PPPB1PBP/R2QKbR1 b Q - 8 9
        split_fen = fen.split(" ")
        self.parse_ranks(split_fen[0])
        
        # white_to_move is set to True on init, so we only need to check if it's black move
        if split_fen[1] == "b":
            self.white_to_move = False
        
        self.parse_castling(split_fen[2])
        self.en_passant_target_square = split_fen[3]
    
    def parse_ranks(self, ranks):
        pass
    
    def parse_castling(self, castling_rights):
        pass  
            
        
        

        
