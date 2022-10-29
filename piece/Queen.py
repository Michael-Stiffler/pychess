from piece.Piece import Piece

class Queen(Piece):
    def __init__(self, x, y, color, filename):
        super().__init__(x, y, color, filename)
        
    def get_moves(self, board):
        pass