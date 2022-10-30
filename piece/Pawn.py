from locale import currency
import os
import sys

from piece.Piece import Piece
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dir_path, os.pardir)))

from board.AlgebraicNotation import AlgebraicNotation


#from board.AlgebraicNotation import AlgebraicNotation

class Pawn(Piece):
    def __init__(self, x, y, color, filename):
        super().__init__(x, y, color, filename)
        self.an = AlgebraicNotation()
        self.moves = []
        self.moves_no_algebraic_notation = []

        
    def get_moves(self, board):
        self.moves = []
        current_position = (self.x, self.y)

        if self.color == self.WHITE:
            first_possible_move = (self.x, self.y-1)
            if board[first_possible_move[1]][first_possible_move[0]] is None:
                self.moves.append(self.an.get_pawn_algebraic_notation(current_position, first_possible_move, False))
                self.moves_no_algebraic_notation.append(first_possible_move)
            if self.y == 6:
                second_possible_move = (self.x, self.y-2)
                if board[second_possible_move[1]][second_possible_move[0]] is None:
                    self.moves.append(self.an.get_pawn_algebraic_notation(current_position, second_possible_move, False))
                    self.moves_no_algebraic_notation.append(second_possible_move)
        elif self.color == self.BLACK:
            first_possible_move = (self.x, self.y+1)
            if board[first_possible_move[1]][first_possible_move[0]] is None:
                self.moves.append(self.an.get_pawn_algebraic_notation(current_position, first_possible_move, False))
                self.moves_no_algebraic_notation.append(first_possible_move)

            if self.y == 1:
                second_possible_move = (self.x, self.y+2)
                if board[second_possible_move[1]][second_possible_move[0]] is None:
                    self.moves.append(self.an.get_pawn_algebraic_notation(current_position, second_possible_move, False))
                    self.moves_no_algebraic_notation.append(second_possible_move)
                    
        return self.moves
        
        