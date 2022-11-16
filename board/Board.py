import math
from piece.Bishop import Bishop
from piece.King import King
from piece.Knight import Knight
from piece.Pawn import Pawn
from piece.Queen import Queen
from piece.Rook import Rook
import board.DrawBoard as db
from board.AlgebraicNotation import AlgebraicNotation
from iteration_utilities import duplicates
import pickle
import sys

class Board():
    
    def __init__(self, display, fen):
        #constants. SIZE is pixel LENGTH of each square on the board and LENGTH is how many squares per column or row.
        self.SIZE = 100
        self.LENGTH = 8
        self.WHITE = 0
        self.BLACK = 1
        
        #self explanatory
        self.pieces_on_board = []
        self.copy_of_pieces_on_board = []
        self.list_of_all_moves = []
        self.list_of_enemy_attack_moves = []
        self.color_to_move = self.WHITE
        self.en_passant_possible = False
        self.en_passant_target_square = ""
        self.en_passant_destination_square = None
        self.copy_of_en_passant_target_square = ""
        self.copy_of_en_passant_destination_square = None
        self.move_is_castle = False
        self.is_enpassant = False
        self.copy_of_is_enpassant = False
        self.fen = fen 
        self.an = AlgebraicNotation()
        self.display = display
        
        #holds the board with all the squares and if there is a piece then an object is there, else it is NoneType
        self.board = [[None for i in range(self.LENGTH)] for j in range(self.LENGTH)]
        self.copy_of_board = [[None for i in range(self.LENGTH)] for j in range(self.LENGTH)]
        
    def get_board(self):
        return self.board

    def get_copy_board(self):
        return self.copy_of_board
    
    def set_copy_board(self, board):
        self.copy_of_board = board

    def get_copy_pieces_on_board(self):
        return self.copy_of_pieces_on_board
    
    def set_copy_pieces_on_board(self, pieces_on_board):
        self.copy_of_pieces_on_board = pieces_on_board
    
    def get_moves(self):
        return self.list_of_all_moves
    
    def get_pieces_on_board(self):
        return self.pieces_on_board
    
    def white_to_move(self):
        return True if self.color_to_move == self.WHITE else False
        
    def draw_board(self):
        db.draw_board(self.display)
                        
    def load_pieces(self):
        db.load_pieces()
            
    def draw_pieces(self):
        db.draw_pieces(self.board, self.display)
    
    def drag_piece(self, mouse_pos):
        db.drag_piece(mouse_pos, self.board, self.display)
        
    def draw_moves(self):
        db.draw_moves(self.display)
        
    def initialize_show_square(self):
        db.initialize_show_square(self.display)
        
    def show_square(self, mouse_position):
        db.show_square(mouse_position, self.display)
        
    def piece_held(self, piece_held):
        db.piece_held = piece_held
                    
    def get_square_from_mouse_pos(self, mouse_pos):
        return (math.floor(mouse_pos[0] / self.SIZE), math.floor(mouse_pos[1] / self.SIZE))
    
    def return_piece_on_square(self, square_coordinates, board = None):
        if board is None:
            board = self.board
        return board[square_coordinates[1]][square_coordinates[0]]                        
        
    def get_check_moves(self, board, pieces_on_board):
        self.list_of_enemy_attack_moves = []
        not_attack_moves = []
        self.color_to_move = self.BLACK if self.color_to_move == self.WHITE else self.WHITE
        for piece in pieces_on_board:
            if piece.color == self.color_to_move:
                if isinstance(piece, Pawn):
                    if self.en_passant_possible:
                        piece.calculate_moves(board, self.copy_of_en_passant_target_square)
                    else:
                        piece.calculate_moves(board)
                    not_attack_moves = piece.get_not_attack_moves()
                    self.en_passant_possible = False
                else:
                    piece.calculate_moves(board)
                    
                moves = piece.get_moves_no_algebraic_notation()
                if moves:
                    for move in moves:
                        if move not in not_attack_moves:
                            self.list_of_enemy_attack_moves.append(move)
        self.color_to_move = self.BLACK if self.color_to_move == self.WHITE else self.WHITE

    def king_in_check(self, board):
        for attack_move in self.list_of_enemy_attack_moves:
            if isinstance(board[attack_move[1]][attack_move[0]], King) and board[attack_move[1]][attack_move[0]].color == self.color_to_move:
                return True
        return False
        
    def check_legal_moves(self, piece, board, pieces_on_board):  
        legal_moves = []
        not_legal_moves = []
        not_legal_moves_an = []
                
        if isinstance(piece, Pawn):
            if self.en_passant_possible:
                piece.calculate_moves(board, self.en_passant_target_square)
            else:
                piece.calculate_moves(board)
            self.en_passant_possible = False
        else:
            piece.calculate_moves(board)
            
        moves = piece.get_moves()
        #print(f"moves {moves}")

        for move in moves:
            self.copy_of_board = pickle.loads(pickle.dumps(board, -1))
            self.copy_of_pieces_on_board = pickle.loads(pickle.dumps(pieces_on_board, -1))
            start_square = (piece.x, piece.y)
            end_square = self.an.get_square_from_algebraic_notation(move)
            if len(move) == 4 and self.an.get_pawn_algebraic_notation(start_square, end_square, False) == self.copy_of_en_passant_target_square and self.return_piece_on_square(end_square, board=board) is None:
                self.copy_of_is_enpassant = True
            self.make_move(move, piece, board=self.copy_of_board, pieces_on_board=self.copy_of_pieces_on_board)
            self.get_check_moves(self.copy_of_board, self.copy_of_pieces_on_board)
            if not self.king_in_check(self.copy_of_board):
                legal_moves.append(move)
            else:
                not_legal_moves.append(move)
                not_legal_moves_an.append(self.an.get_square_from_algebraic_notation(move))
        piece.moves = list(set(piece.get_moves())-set(not_legal_moves))
        piece.moves_no_algebraic_notation = list(set(piece.get_moves_no_algebraic_notation())-set(not_legal_moves_an))
        return legal_moves
    
    def check_if_game_over(self, move, piece, board, pieces_on_board):
        self.copy_of_board = pickle.loads(pickle.dumps(board, -1))
        self.copy_of_pieces_on_board = pickle.loads(pickle.dumps(pieces_on_board, -1))
        self.make_move(move, piece, board=self.copy_of_board, pieces_on_board=self.copy_of_pieces_on_board)
        moves = []
        self.switch_color_to_move()
    
        for piece in pieces_on_board:
            if piece.color == self.color_to_move:
                moves.extend(self.check_legal_moves(piece, self.copy_of_board, self.copy_of_pieces_on_board))
                                        
        if len(moves) == 0:
            if self.king_in_check(board):
                return "checkmate"
            else:
                return "stalemate"
        if self.king_in_check(board):
            return "in check"
        return ""
        
    def get_piece_moves(self, board=None, pieces_on_board=None):        
        actual_move = False
        
        if board is None:
            actual_move = True
            board = self.board
        
        if pieces_on_board is None:
            pieces_on_board = self.pieces_on_board
        
        self.list_of_all_moves = []
        self.list_of_enemy_attack_moves = []
        duplicate_move_to_fixed_dict = {}

        for piece in pieces_on_board:
            if piece.color == self.color_to_move:
                moves = self.check_legal_moves(piece, board, pieces_on_board)
                if moves:
                    for move in moves:
                        self.list_of_all_moves.append(move)
                        game_over = self.check_if_game_over(move=move, piece=piece, board=board, pieces_on_board=pieces_on_board)
                        self.switch_color_to_move()
                        if game_over == "stalemate":
                            new_move = move + "$"
                            duplicate_move_to_fixed_dict[move] = new_move
                            self.list_of_all_moves.remove(move) 
                            self.list_of_all_moves.append(new_move) 
                        elif game_over == "checkmate":
                            new_move = move + "#"
                            duplicate_move_to_fixed_dict[move] = new_move
                            self.list_of_all_moves.remove(move) 
                            self.list_of_all_moves.append(new_move)  
                        elif game_over == "in check": 
                            new_move = move + "+"
                            duplicate_move_to_fixed_dict[move] = new_move
                            self.list_of_all_moves.remove(move) 
                            self.list_of_all_moves.append(new_move)    
                                     
                                                                                              
        if len(self.list_of_all_moves) == 0 and actual_move:
            if self.king_in_check(board):
                print("Checkmate!")
            else:
                print("Stalemate!")
            sys.exit()
                    
        move_duplicates = list(duplicates(self.list_of_all_moves))
        #print(f"duplicates: {move_duplicates}")

        for move in self.list_of_all_moves:
            if move in move_duplicates:
                self.list_of_all_moves.remove(move) 
        
        fixed_move_duplicates = self.parse_duplicate_moves(move_duplicates)
        self.list_of_all_moves.extend(fixed_move_duplicates)
        #print(f"moves: {self.list_of_all_moves}")
        
        for move in move_duplicates:
            duplicate_move_to_fixed_dict[move] = [x for x in fixed_move_duplicates if move[0] == x[0] and move[-1] == x[-1] and move[-2] == x[-2]]
            
        for piece in pieces_on_board:
            for move in duplicate_move_to_fixed_dict:
                if move in piece.moves:
                    piece.moves.remove(move)
                    piece.moves.append(duplicate_move_to_fixed_dict[move])
                    
        #print(self.list_of_all_moves)
                    
    def parse_duplicate_moves(self, duplicate_moves):
        changed_moves = []
        
        for move in duplicate_moves:
            piece_letter = move[0]
            for piece in self.pieces_on_board:
                if isinstance(piece, Rook) and piece.color == self.color_to_move and piece_letter == 'R':
                    if self.is_piece_on_same_file(piece, Rook):
                        changed_moves.append(move[0] + str(self.an.get_file_number(piece.y)) + move[1:])
                    elif self.is_piece_on_same_rank(piece, Rook):
                        changed_moves.append(move[0] + str(self.an.get_rank_letter(piece.x)) + move[1:])
                elif isinstance(piece, Queen) and piece.color == self.color_to_move and piece_letter == 'Q':
                    if self.is_piece_on_same_file(piece, Queen):
                        changed_moves.append(move[0] + str(self.an.get_file_number(piece.y)) + move[1:])
                    else:
                        changed_moves.append(move[0] + str(self.an.get_rank_letter(piece.x)) + move[1:])
                elif isinstance(piece, Knight) and piece.color == self.color_to_move and piece_letter == 'N':
                    changed_moves.append(move[0] + str(self.an.get_rank_letter(piece.x)) + move[1:])
                elif isinstance(piece, Bishop) and piece.color == self.color_to_move and piece_letter == 'B':
                    changed_moves.append(move[0] + str(self.an.get_rank_letter(piece.x)) + move[1:])
                    
        return changed_moves       

                                
    def is_piece_on_same_file(self, piece, piece_class):
        for y in range(self.LENGTH):
            if y == piece.y:
                continue
            square_on_file = self.board[y][piece.x]
            if isinstance(square_on_file, piece_class) and square_on_file.color == piece.color:
                    return True
        return False
    
    def is_piece_on_same_rank(self, piece, piece_class):
        for x in range(self.LENGTH):
            if x == piece.x:
                continue
            square_on_rank = self.board[piece.y][x]
            if isinstance(square_on_rank, piece_class) and isinstance(piece, piece_class) and square_on_rank.color == piece.color:
                    return True
        return False

            
    def check_user_move(self, start_square, end_square): 
        alternate_moves = []
              
        piece = self.board[start_square[1]][start_square[0]]
        destination = self.board[end_square[1]][end_square[0]]
        #if the user selected a square with a piece
        if piece and piece.color == self.color_to_move:  
            #only 2* options on a move. Piece ends on an empty square, or it lands on a piece of another color (capture)
            if destination is None or piece.color != destination.color:
                is_capture = True if destination != None else False  # if the destination square is a piece, it will be a capture
                
                if isinstance(piece, Pawn):
                    if self.an.get_pawn_algebraic_notation(start_square, end_square, False) == self.en_passant_target_square:
                        move = self.an.get_pawn_algebraic_notation(start_square, end_square, True)
                        self.is_enpassant = True
                    elif (piece.y == 1 and piece.color == self.WHITE) or (piece.y == 6 and piece.color == self.BLACK):
                        move = self.an.get_pawn_promotion_notation(start_square, end_square, is_capture)
                    else:
                        move = self.an.get_pawn_algebraic_notation(start_square, end_square, is_capture)
                elif isinstance(piece, Knight):
                    move = self.an.get_knight_algebraic_notation(start_square, end_square, is_capture)
                    alternate_moves.append(move[0] + str(self.an.get_rank_letter(piece.x)) + move[1:])
                elif isinstance(piece, Bishop):
                    move = self.an.get_bishop_algebraic_notation(start_square, end_square, is_capture)
                    alternate_moves.append(move[0] + str(self.an.get_rank_letter(piece.x)) + move[1:])
                elif isinstance(piece, Queen):
                    move = self.an.get_queen_algebraic_notation(start_square, end_square, is_capture)
                    alternate_moves.append(move[0] + str(self.an.get_file_number(piece.y)) + move[1:])
                    alternate_moves.append(move[0] + str(self.an.get_rank_letter(piece.x)) + move[1:])
                elif isinstance(piece, Rook):
                    move = self.an.get_rook_algebraic_notation(start_square, end_square, is_capture)
                    alternate_moves.append(move[0] + str(self.an.get_file_number(piece.y)) + move[1:])
                    alternate_moves.append(move[0] + str(self.an.get_rank_letter(piece.x)) + move[1:])
                elif isinstance(piece, King):
                    if piece.color == self.WHITE and start_square == (4,7) and end_square == (6,7):
                        move = self.an.get_king_castle_notation(True)
                    elif piece.color == self.WHITE and start_square == (4,7) and end_square == (2,7):
                        move = self.an.get_king_castle_notation(False)
                    elif piece.color == self.BLACK and start_square == (4,0) and end_square == (6,0):
                        move = self.an.get_king_castle_notation(True)
                    elif piece.color == self.BLACK and start_square == (4,0) and end_square == (2,0):
                        move = self.an.get_king_castle_notation(False)
                    else:
                        move = self.an.get_king_algebraic_notation(start_square, end_square, is_capture)
                
                alternate_moves.append(move + "$")
                alternate_moves.append(move + "#")
                alternate_moves.append(move + "+")        
        
                if move in piece.moves:
                    if move == "O-O" or move == "O-O-O":
                        self.move_is_castle = True
                    return move
                else:
                    for alterate_move in alternate_moves:
                        if alterate_move in piece.moves:
                            return alterate_move
                return None
    
    def make_pawn_move(self, move, piece, board, pieces_on_board, start_square, destination_square, piece_on_start_square, piece_on_destination_square, actual_move):  
        # this is for setting the enpassant square
        if (self.is_enpassant and actual_move) or (self.copy_of_is_enpassant and not actual_move):
            board[destination_square[1]][destination_square[0]] = piece_on_start_square
            board[start_square[1]][start_square[0]] = None
            if actual_move:
                pawn_to_remove = self.return_piece_on_square(self.en_passant_destination_square, board)
            else:
                pawn_to_remove = self.return_piece_on_square(self.copy_of_en_passant_destination_square, board)
            for same_piece in pieces_on_board:
                if same_piece.color == pawn_to_remove.color and (same_piece.x, same_piece.y) == (pawn_to_remove.x, pawn_to_remove.y):
                    pieces_on_board.remove(same_piece)
                    break
            board[pawn_to_remove.y][pawn_to_remove.x] = None
        else:
            if board[destination_square[1]][destination_square[0]] is not None:
                for same_piece in pieces_on_board:
                    if same_piece.color == piece_on_destination_square.color and (same_piece.x, same_piece.y) == (piece_on_destination_square.x, piece_on_destination_square.y):
                        pieces_on_board.remove(same_piece)
                        break
                board[destination_square[1]][destination_square[0]] = piece_on_start_square
                board[start_square[1]][start_square[0]] = None
            else:
                board[destination_square[1]][destination_square[0]] = piece_on_start_square
                board[start_square[1]][start_square[0]] = None 

            for p in pieces_on_board:
                if p.color == piece_on_start_square.color and (p.x, p.y) == (piece_on_start_square.x, piece_on_start_square.y):
                    p.x = destination_square[0]
                    p.y = destination_square[1]
                    
            board[destination_square[1]][destination_square[0]].x = destination_square[0]
            board[destination_square[1]][destination_square[0]].y = destination_square[1]
        if piece_on_start_square.color == self.WHITE:
            if start_square[1] - 2 == destination_square[1]:
                if not actual_move:
                    self.copy_of_en_passant_target_square = self.an.get_pawn_algebraic_notation(start_square, (start_square[0], start_square[1] - 1), False)
                    self.copy_of_en_passant_destination_square = destination_square
                else:
                    self.en_passant_target_square = self.an.get_pawn_algebraic_notation(start_square, (start_square[0], start_square[1] - 1), False)
                    self.en_passant_destination_square = destination_square 
                self.en_passant_possible = True 
        else:
            if start_square[1] + 2 == destination_square[1]:
                if not actual_move:
                    self.copy_of_en_passant_target_square = self.an.get_pawn_algebraic_notation(start_square, (start_square[0], start_square[1] + 1), False)
                    self.copy_of_en_passant_destination_square = destination_square
                else:
                    self.en_passant_target_square = self.an.get_pawn_algebraic_notation(start_square, (start_square[0], start_square[1] + 1), False)
                    self.en_passant_destination_square = destination_square
                self.en_passant_possible = True 

        if self.is_enpassant:
            self.is_enpassant = False
            self.en_passant_target_square = ""
            self.en_passant_destination_square = None
        if self.copy_of_is_enpassant:
            self.copy_of_is_enpassant = False
            self.copy_of_en_passant_target_square = ""
            self.copy_of_en_passant_destination_square = None    
        
        if "=" in move:
            self.promote_to_queen(piece_on_start_square, board, pieces_on_board)   
            
    
    def make_king_move(self, move, piece, board, pieces_on_board, start_square, destination_square, piece_on_start_square, piece_on_destination_square, actual_move):
        if self.move_is_castle:
            piece_on_start_square.can_castle_kingside = False
            piece_on_start_square.can_castle_queenside = False
            board[destination_square[1]][destination_square[0]] = piece_on_start_square
            board[start_square[1]][start_square[0]] = None
            
            if piece_on_start_square.color == self.WHITE and start_square == (4,7) and destination_square == (6,7):
                rook = board[7][7]
                rook.x = 5 
                rook.y = 7 
                board[7][5] = rook
                board[7][7] = None
            elif piece_on_start_square.color == self.WHITE and start_square == (4,7) and destination_square == (2,7):
                rook = board[7][0]
                rook.x = 3 
                rook.y = 7 
                board[7][3] = rook
                board[7][0] = None
            elif piece_on_start_square.color == self.BLACK and start_square == (4,0) and destination_square == (6,0):
                rook = board[0][7]
                rook.x = 5 
                rook.y = 0 
                board[0][5] = rook
                board[0][7] = None
            elif piece_on_start_square.color == self.BLACK and start_square == (4,0) and destination_square == (2,0):
                rook = board[0][0]
                rook.x = 3
                rook.y = 0 
                board[0][3] = rook
                board[0][0] = None
            self.move_is_castle = False
        else: 
            if board[destination_square[1]][destination_square[0]] is not None:
                for same_piece in pieces_on_board:
                    if same_piece.color == board[destination_square[1]][destination_square[0]].color and (same_piece.x, same_piece.y) == (board[destination_square[1]][destination_square[0]].x, board[destination_square[1]][destination_square[0]].y):
                        pieces_on_board.remove(same_piece)
                        break
                board[destination_square[1]][destination_square[0]] = piece_on_start_square
                board[start_square[1]][start_square[0]] = None
            else:
                board[destination_square[1]][destination_square[0]] = piece_on_start_square
                board[start_square[1]][start_square[0]] = None 
        for p in pieces_on_board:
            if p.color == piece_on_start_square.color and (p.x, p.y) == (piece_on_start_square.x, piece_on_start_square.y):
                p.x = destination_square[0]
                p.y = destination_square[1]

        board[destination_square[1]][destination_square[0]].x = destination_square[0]
        board[destination_square[1]][destination_square[0]].y = destination_square[1]
        
                                    
    def make_move(self, move, piece, board=None, pieces_on_board=None):
        actual_move = False
        
        if board is None:
            board = self.board
            actual_move = True
            
        if pieces_on_board is None:
            pieces_on_board = self.pieces_on_board
                 
        start_square = (piece.x, piece.y)
        
        if move == "O-O" or move == "O-O-O":
            destination_square = self.an.get_castle_square_from_algebraic_notation(move, piece)
        else:
            destination_square = self.an.get_square_from_algebraic_notation(move)
            
        piece_on_destination_square = self.return_piece_on_square(destination_square, board)
        piece_on_start_square = self.return_piece_on_square(start_square, board)
        
        if piece_on_destination_square:
            for p in pieces_on_board:
                if p.color ==  piece_on_destination_square.color and (p.y, p.x) == (piece_on_destination_square.y, piece_on_destination_square.x):
                    pieces_on_board.remove(p)
              
        if isinstance(piece, Pawn):
            self.make_pawn_move(move, piece, board, pieces_on_board, start_square, destination_square, piece_on_start_square, piece_on_destination_square, actual_move)
        elif isinstance(piece, King):
            self.make_king_move(move, piece, board, pieces_on_board, start_square, destination_square, piece_on_start_square, piece_on_destination_square, actual_move)
        else:       
            if board[destination_square[1]][destination_square[0]] is not None:
                for same_piece in pieces_on_board:
                    if same_piece.color == piece_on_destination_square.color and (same_piece.x, same_piece.y) == (piece_on_destination_square.x, piece_on_destination_square.y):
                        pieces_on_board.remove(same_piece)
                        break
                board[destination_square[1]][destination_square[0]] = piece_on_start_square
                board[start_square[1]][start_square[0]] = None
            else:
                board[destination_square[1]][destination_square[0]] = piece_on_start_square
                board[start_square[1]][start_square[0]] = None 
            
            for p in pieces_on_board:
                if p.color == piece_on_start_square.color and (p.x, p.y) == (piece_on_start_square.x, piece_on_start_square.y):
                    p.x = destination_square[0]
                    p.y = destination_square[1]
            board[destination_square[1]][destination_square[0]].x = destination_square[0]
            board[destination_square[1]][destination_square[0]].y = destination_square[1]
            
    def switch_color_to_move(self):
        self.color_to_move = self.BLACK if self.color_to_move == self.WHITE else self.WHITE 
  
    def parse_fen(self):
        
        # parse fen from this -> rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
        # to this -> ['rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR', 'w', 'KQkq', '-', '0', '1']
        
        #Handle each part of the fen (in the list) with the following
        
        #For now I am ignoring fullmove counter and halfmove clock

        split_fen = self.fen.split(" ")
        self.parse_ranks_on_fen(split_fen[0])
        
        # color_to_move is set to True on init, so we only need to check if it's black move
        if split_fen[1] == "b":
            self.color_to_move = self.BLACK
        
        self.parse_castling_on_fen(split_fen[2])
        self.en_passant_target_square = split_fen[3] if split_fen[3] != "-" else ""
    
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
                        self.board[y][x] = pawn
                        self.pieces_on_board.append(pawn)
                    else:
                        pawn = Pawn(x, y, self.BLACK, filename="bP")
                        self.board[y][x] = pawn
                        self.pieces_on_board.append(pawn)
                elif piece_positions[index].lower() == "n":
                    if piece_positions[index].isupper():
                        knight = Knight(x, y, self.WHITE, filename="wN")
                        self.board[y][x] = knight
                        self.pieces_on_board.append(knight)
                    else:
                        knight = Knight(x, y, self.BLACK, filename="bN")
                        self.board[y][x] = knight
                        self.pieces_on_board.append(knight)
                elif piece_positions[index].lower() == "b":
                    if piece_positions[index].isupper():
                        bishop = Bishop(x, y, self.WHITE, filename="wB")
                        self.board[y][x] = bishop
                        self.pieces_on_board.append(bishop)
                    else:
                        bishop = Bishop(x, y, self.BLACK, filename="bB")
                        self.board[y][x] = bishop
                        self.pieces_on_board.append(bishop)
                elif piece_positions[index].lower() == "q":
                    if piece_positions[index].isupper():
                        queen = Queen(x, y, self.WHITE, filename="wQ")
                        self.board[y][x] = queen
                        self.pieces_on_board.append(queen)
                    else:
                        queen = Queen(x, y, self.BLACK, filename="bQ")
                        self.board[y][x] = queen
                        self.pieces_on_board.append(queen)
                elif piece_positions[index].lower() == "k":
                    if piece_positions[index].isupper():
                        king = King(x, y, self.WHITE, filename="wK")
                        self.board[y][x] = king
                        self.pieces_on_board.append(king)
                    else:
                        king = King(x, y, self.BLACK, filename="bK")
                        self.board[y][x] = king
                        self.pieces_on_board.append(king)
                elif piece_positions[index].lower() == "r":
                    if piece_positions[index].isupper():
                        rook = Rook(x, y, self.WHITE, filename="wR")
                        self.board[y][x] = rook
                        self.pieces_on_board.append(rook)
                    else:
                        rook = Rook(x, y, self.BLACK, filename="bR")
                        self.board[y][x] = rook
                        self.pieces_on_board.append(rook)      
                                  
            
    def parse_castling_on_fen(self, castling_rights):
        kings = [self.board[y][x] for x in range(self.LENGTH) for y in range(self.LENGTH) if isinstance(self.board[y][x], King)]
        for king in kings:
            if king.color == self.WHITE and "K" not in castling_rights:
                king.can_castle_kingside = False
            if king.color == self.WHITE and "Q" not in castling_rights:
                king.can_castle_queenside = False
            if king.color == self.BLACK and "k" not in castling_rights:
                king.can_castle_kingside = False
            if king.color == self.BLACK and "q" not in castling_rights:
                king.can_castle_queenside = False
                
    def promote_to_queen(self, piece, board, pieces_on_board):
        board[piece.y][piece.x] = Queen(piece.x, piece.y, self.WHITE, filename="wQ") if piece.color == self.WHITE else Queen(piece.x, piece.y, self.BLACK, filename="bQ")
        for same_piece in pieces_on_board:
            if piece.color == same_piece.color and (piece.x, piece.y) == (same_piece.x, same_piece.y):
                pieces_on_board.remove(same_piece)
                pieces_on_board.append(board[piece.y][piece.x])
                break

        
    def promote_to_rook(self, piece):
        pass
    
    def promote_to_bishop(self, piece):
        pass
    
    def promote_to_knight(self, piece):
        pass
                    
                    
                      
            
        
        

        
