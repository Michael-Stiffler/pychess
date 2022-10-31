import os
import sys

from piece.Piece import Piece
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dir_path, os.pardir)))

from board.AlgebraicNotation import AlgebraicNotation

class King(Piece):
    def __init__(self, x, y, color, filename):
        super().__init__(x, y, color, filename)
        can_castle_queenside = True
        can_castle_kingside = True
        self.an = AlgebraicNotation()
        self.moves = []
        self.moves_no_algebraic_notation = []
        
    def get_moves(self, board):
        self.moves = []
        self.moves_no_algebraic_notation = []
        current_position = (self.x, self.y)
        
        for x in range(-1,2):
            for y in range(-1,2):
                if x == 0 and y == 0:
                    continue
                move = (self.x+x, self.y+y)
                if move[0] >= 0 and move[0] <= 7 and move[1] >= 0 and move[1] <= 7:
                    if board[move[1]][move[0]] is None:
                        self.moves.append(self.an.get_king_algebraic_notation(current_position, move, False))
                        self.moves_no_algebraic_notation.append(move)
                    elif board[move[1]][move[0]].color != self.color:
                        self.moves.append(self.an.get_king_algebraic_notation(current_position, move, True))
                        self.moves_no_algebraic_notation.append(move)

                    
        return self.moves