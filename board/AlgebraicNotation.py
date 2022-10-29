from piece.Bishop import Bishop
from piece.King import King
from piece.Knight import Knight
from piece.Pawn import Pawn
from piece.Queen import Queen
from piece.Rook import Rook


class AlgebraicNotation():
    def __init__(self):
        self.files = [x for x in range(1, 9)]
        self.ranks = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        
    def get_pawn_algebraic_notation():
        pass
    
    def get_piece_algebraic_notation(self, piece, start, end, is_capture, is_same_piece_on_rank, is_same_piece_on_file):
        #TODO: implement
        
        if isinstance(piece, Pawn):
            return self.get_pawn_algebraic_notation(start, end, is_capture)
        elif isinstance(piece, Knight):
            return self.get_knight_algebraic_notation(start, end, is_capture, is_same_piece_on_rank, is_same_piece_on_file)
        elif isinstance(piece, Bishop):
            return self.get_bishop_algebraic_notation(start, end, is_capture, is_same_piece_on_rank, is_same_piece_on_file)
        elif isinstance(piece, Queen):
            return self.get_queen_algebraic_notation(start, end, is_capture, is_same_piece_on_rank, is_same_piece_on_file)
        elif isinstance(piece, Rook):
            return self.get_rook_algebraic_notation(start, end, is_capture, is_same_piece_on_rank, is_same_piece_on_file)
        elif isinstance(piece, King):
            return self.get_king_algebraic_notation(start, end, is_capture)
        
    def get_pawn_algebraic_notation(self, start, end, is_capture):
        #TODO EN PASSANT
        
        if not is_capture:
            return f"{self.get_rank_letter(end[0])}{self.get_file_number(end[1])}"
        else:
            return f"{self.get_rank_letter(start[0])}x{self.get_rank_letter(end[0])}{self.get_file_number(end[1])}"
    
    def get_knight_algebraic_notation(self, start, end, is_capture, is_same_piece_on_rank, is_same_piece_on_file):
        #TODO taking care of knights on same rank and file that can move to same spot
        
        if not is_capture:
            return f"N{self.get_rank_letter(end[0])}{self.get_file_number(end[1])}"
        else:
            return f"Nx{self.get_rank_letter(end[0])}{self.get_file_number(end[1])}"
    
    def get_bishop_algebraic_notation(self, start, end, is_capture, is_same_piece_on_rank, is_same_piece_on_file):
        #TODO taking care of bishops on same rank and file that can move to same spot
        
        if not is_capture:
            return f"B{self.get_rank_letter(end[0])}{self.get_file_number(end[1])}"
        else:
            return f"Bx{self.get_rank_letter(end[0])}{self.get_file_number(end[1])}"
    
    def get_queen_algebraic_notation(self, start, end, is_capture, is_same_piece_on_rank, is_same_piece_on_file):
        #TODO taking care of bishops on same rank and file that can move to same spot

        if not is_capture:
            return f"Q{self.get_rank_letter(end[0])}{self.get_file_number(end[1])}"
        else:
            return f"Qx{self.get_rank_letter(end[0])}{self.get_file_number(end[1])}"
    
    def get_rook_algebraic_notation(self, start, end, is_capture, is_same_piece_on_rank, is_same_piece_on_file):
        #TODO taking care of bishops on same rank and file that can move to same spot
        
        if not is_capture:
            return f"R{self.get_rank_letter(end[0])}{self.get_file_number(end[1])}"
        else:
            return f"Rx{self.get_rank_letter(end[0])}{self.get_file_number(end[1])}"
    
    def get_king_algebraic_notation(self, start, end, is_capture):
        #TODO castling

        if not is_capture:
            return f"K{self.get_rank_letter(end[0])}{self.get_file_number(end[1])}"
        else:
            return f"Kx{self.get_rank_letter(end[0])}{self.get_file_number(end[1])}"
    
    def get_rank_letter(self, num):
        return self.ranks[num]
    
    def get_file_number(self, num):
        return self.files[-(num + 1)]

    