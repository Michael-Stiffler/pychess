from piece.Piece import Piece

class King(Piece):
    def __init__(self, x, y, color, filename):
        super().__init__(x, y, color, filename)
        self.can_castle_queenside = True
        self.can_castle_kingside = True
        
    def get_moves():
        pass