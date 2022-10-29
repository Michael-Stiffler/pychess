from piece.Piece import Piece
from better-chess.board.AlgebraicNotation import AlgebraicNotation 
#from board.AlgebraicNotation import AlgebraicNotation

class Pawn(Piece):
    def __init__(self, x, y, color, filename):
        super().__init__(x, y, color, filename)
        self.an = AlgebraicNotation()

        
    def get_moves(self, board):
        moves = []
        
        if self.color == self.WHITE:
            if board[self.x][self.y-1]:
               pass 
        else:
            pass
        
        