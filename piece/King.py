from piece.Piece import Piece

class King(Piece):
    def __init__(self, x, y, color, filename):
        super().__init__(x, y, color, filename)
        can_castle_queenside = True
        can_castle_kingside = True
        
    def get_moves(self, board):
        pass