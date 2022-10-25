import pygame as py
import math
import os
from piece.Bishop import Bishop
from piece.King import King
from piece.Knight import Knight
from piece.Pawn import Pawn
from piece.Queen import Queen
from piece.Rook import Rook
from board.AlgebraicNotation import AlgebraicNotation

class Board():
    
    def __init__(self, display, fen):
        #constants. SIZE is pixel LENGTH of each square on the board and LENGTH is how many squares per column or row.
        self.SIZE = 100
        self.LENGTH = 8
        self.WHITE = 0
        self.BLACK = 1
        self.IMAGES = {}
        
        #self explanatory
        self.pieces_on_board = []
        self.list_of_all_moves = []
        self.white_to_move = True
        self.en_passant_target_square = ""
        self.current_user_square = None
        self.display = display       
        self.fen = fen 
        self.an = AlgebraicNotation()
        
        #holds the board with all the squares and if there is a piece then an object is there, else it is NoneType
        self.board = [[None for i in range(self.LENGTH)] for j in range(self.LENGTH)]
        
        #colors for black and white squares as well as the highlight color
        self.whiteColor = (255, 255, 255, 255)
        self.blackColor =  (205, 129, 70, 255)
        self.highlight_color = (101, 67, 45, 140)
        
        #set a pygame surface object for a square on the board with alpha and keep that square
        self.square_surface = py.Surface((100,100), py.SRCALPHA)      
        self.square_surface_rect = self.square_surface.get_rect(topleft=(0,0))

    
    def draw_board(self):
    
        count = 0
        for x in range(1, self.LENGTH + 1):
            for y in range(1, self.LENGTH + 1):
                if count % 2 == 0:
                    py.draw.rect(self.display, self.whiteColor, [
                                self.SIZE*y - self.SIZE, self.SIZE*x - self.SIZE, self.SIZE, self.SIZE])
                else:
                    py.draw.rect(self.display, self.blackColor, [
                                self.SIZE*y - self.SIZE, self.SIZE*x - self.SIZE, self.SIZE, self.SIZE])
                count += 1
            count -= 1
                        
    def load_pieces(self):
        pieces = ['bB', 'bK', 'bN', 'bP', 'bQ',
                 'bR', 'wB', 'wK', 'wN', 'wP', 'wQ', 'wR']
        for piece in pieces:
            source_file_dir = os.path.dirname(os.path.abspath(os.getcwd()))
            image_path = os.path.join(source_file_dir, "better-chess\\piece_images\\" + piece + '.png')
            self.IMAGES[piece] = py.transform.scale(py.image.load(image_path), (self.SIZE, self.SIZE))
            
    def draw_pieces(self):
        for x in range(self.LENGTH):
            for y in range(self.LENGTH):
                piece = self.board[y][x]
                if piece:
                    self.display.blit(self.IMAGES[piece.filename], py.Rect(y*self.SIZE, x*self.SIZE, self.SIZE, self.SIZE))
                    
    def show_square(self, mouse_position):
        # this is for debugging purposes
        
        #formatted user position. ie (0,1), (2,2), etc
        square_postion_x, square_position_y = (math.floor(mouse_position[0] / self.SIZE), math.floor(mouse_position[1] / self.SIZE))
        
        #we want to check if the square the user is currently at is different than the last. 
        #helps not run through this process
        if self.current_user_square is None or self.current_user_square[0] != square_postion_x or self.current_user_square[1] != square_position_y:
            
            #draw the pieces and the board over what we have so it can reset each iteration
            self.draw_board()
            self.draw_pieces()
            
            #set the current_user_square to the one we just moved to
            self.current_user_square = (square_postion_x, square_position_y)
            #find and create the area around where the rectangle should be. ie (100,100), (300,400), etc.
            rect = (self.SIZE*(square_postion_x + 1) - self.SIZE, self.SIZE*(square_position_y + 1) - self.SIZE, self.SIZE, self.SIZE)
            
            #change the current topleft of that rectange to those new values. draw that rectange with a color. blit it on screen.
            self.square_surface_rect.topleft = (rect[0], rect[1])
            self.display.blit(self.square_surface, self.square_surface_rect)  
            
    def initialize_show_square(self):
        py.draw.rect(self.square_surface, self.highlight_color, self.square_surface_rect)
        self.display.blit(self.square_surface, self.square_surface_rect) 
        
    
    def get_piece_moves(self):
        for piece in self.pieces_on_board:
            pass
            
    def check_user_move(self, start_square, end_square):
        #TODO: implement... there is much more to this than I thought lol
        
        #if the user selected a square with a piece
        if self.board[start_square[0]][start_square[1]]:  
            #only 2* options on a move. Piece ends on an empty square, or it lands on a piece of another color (capture)
            if self.board[end_square[0]][end_square[1]] is None or self.board[start_square[0]][start_square[1]].color != self.board[end_square[0]][end_square[1]].color:
                is_capture = True if self.board[end_square[0]][end_square[1]] != None else False  # if the destination square is a piece, it could be a capture
                move = self.an.get_piece_algebraic_notation(start_square, end_square, is_capture)
                if move in self.list_of_all_moves:
                    return move
                return None
        
    def parse_fen(self):
        
        # parse fen from this -> rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
        # to this -> ['rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR', 'w', 'KQkq', '-', '0', '1']
        
        #Handle each part of the fen (in the list) with the following
        
        #For now I am ignoring fullmove counter and halfmove clock

        split_fen = self.fen.split(" ")
        self.parse_ranks_on_fen(split_fen[0])
        
        # white_to_move is set to True on init, so we only need to check if it's black move
        if split_fen[1] == "b":
            self.white_to_move = False
        
        self.parse_castling_on_fen(split_fen[2])
        self.en_passant_target_square = split_fen[3]
    
    def parse_ranks_on_fen(self, ranks):
        piece_positions = []
        ranks = ranks.replace("/", "")
        for x in range(len(ranks)):
            if ranks[x].isalpha():
                piece_positions.append(ranks[x])
            else:
                for y in range(int(ranks[x])):
                    piece_positions.append("0")
    
        for y in range(self.LENGTH):
            for x in range(self.LENGTH):
                index = (y * self.LENGTH) + x
                if piece_positions[index].lower() == "p":
                    if piece_positions[index].isupper():
                        pawn = Pawn(x, y, self.WHITE, filename="wP")
                        self.board[x][y] = pawn
                        self.pieces_on_board.append(pawn)
                    else:
                        pawn = Pawn(x, y, self.BLACK, filename="bP")
                        self.board[x][y] = pawn
                        self.pieces_on_board.append(pawn)
                elif piece_positions[index].lower() == "n":
                    if piece_positions[index].isupper():
                        knight = Knight(x, y, self.WHITE, filename="wN")
                        self.board[x][y] = knight
                        self.pieces_on_board.append(knight)
                    else:
                        knight = Knight(x, y, self.BLACK, filename="bN")
                        self.board[x][y] = knight
                        self.pieces_on_board.append(knight)
                elif piece_positions[index].lower() == "b":
                    if piece_positions[index].isupper():
                        bishop = Bishop(x, y, self.WHITE, filename="wB")
                        self.board[x][y] = bishop
                        self.pieces_on_board.append(bishop)
                    else:
                        bishop = Bishop(x, y, self.BLACK, filename="bB")
                        self.board[x][y] = bishop
                        self.pieces_on_board.append(bishop)
                elif piece_positions[index].lower() == "q":
                    if piece_positions[index].isupper():
                        queen = Queen(x, y, self.WHITE, filename="wQ")
                        self.board[x][y] = queen
                        self.pieces_on_board.append(queen)
                    else:
                        queen = Queen(x, y, self.BLACK, filename="bQ")
                        self.board[x][y] = queen
                        self.pieces_on_board.append(queen)
                elif piece_positions[index].lower() == "k":
                    if piece_positions[index].isupper():
                        king = King(x, y, self.WHITE, filename="wK")
                        self.board[x][y] = king
                        self.pieces_on_board.append(king)
                    else:
                        king = King(x, y, self.BLACK, filename="bK")
                        self.board[x][y] = king
                        self.pieces_on_board.append(king)
                elif piece_positions[index].lower() == "r":
                    if piece_positions[index].isupper():
                        rook = Rook(x, y, self.WHITE, filename="wR")
                        self.board[x][y] = rook
                        self.pieces_on_board.append(rook)
                    else:
                        rook = Rook(x, y, self.BLACK, filename="bR")
                        self.board[x][y] = rook
                        self.pieces_on_board.append(rook)      
                                  
            
    def parse_castling_on_fen(self, castling_rights):
        kings = [self.board[x][y] for x in range(self.LENGTH) for y in range(self.LENGTH) if isinstance(self.board[x][y], King)]
        for king in kings:
            if king.color == self.WHITE and "K" not in castling_rights:
                king.can_castle_kingside = False
            if king.color == self.WHITE and "Q" not in castling_rights:
                king.can_castle_queenside = False
            if king.color == self.BLACK and "k" not in castling_rights:
                king.can_castle_kingside = False
            if king.color == self.BLACK and "q" not in castling_rights:
                king.can_castle_queenside = False
                    
                    
                      
            
        
        

        
