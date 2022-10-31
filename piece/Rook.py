import os
import sys

from piece.Piece import Piece
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dir_path, os.pardir)))

from board.AlgebraicNotation import AlgebraicNotation

class Rook(Piece):
    def __init__(self, x, y, color, filename):
        super().__init__(x, y, color, filename)
        self.an = AlgebraicNotation()
        self.moves = []
        self.moves_no_algebraic_notation = []
        
    def get_moves(self, board):
        self.moves.clear()
        self.moves_no_algebraic_notation.clear()
        current_position = (self.x, self.y)
        
        for x in range(self.x + 1, 8):
            move = (x, self.y)
            if board[move[1]][move[0]] is None:
                self.moves.append(self.an.get_rook_algebraic_notation(current_position, move, False))
                self.moves_no_algebraic_notation.append(move)
            elif board[move[1]][move[0]].color != self.color:
                self.moves.append(self.an.get_rook_algebraic_notation(current_position, move, True))
                self.moves_no_algebraic_notation.append(move)
                break
            elif board[move[1]][move[0]].color == self.color:
                break
            
        for x in range(self.x - 1, -1, -1):
            move = (x, self.y)
            if board[move[1]][move[0]] is None:
                self.moves.append(self.an.get_rook_algebraic_notation(current_position, move, False))
                self.moves_no_algebraic_notation.append(move)
            elif board[move[1]][move[0]].color != self.color:
                self.moves.append(self.an.get_rook_algebraic_notation(current_position, move, True))
                self.moves_no_algebraic_notation.append(move)
                break
            elif board[move[1]][move[0]].color == self.color:
                break
            
        for y in range(self.y + 1, 8):
            move = (self.x, y)
            if board[move[1]][move[0]] is None:
                self.moves.append(self.an.get_rook_algebraic_notation(current_position, move, False))
                self.moves_no_algebraic_notation.append(move)
            elif board[move[1]][move[0]].color != self.color:
                self.moves.append(self.an.get_rook_algebraic_notation(current_position, move, True))
                self.moves_no_algebraic_notation.append(move)
                break
            elif board[move[1]][move[0]].color == self.color:
                break
            
            
        for y in range(self.y - 1, -1, -1):
            move = (self.x, y)
            if board[move[1]][move[0]] is None:
                self.moves.append(self.an.get_rook_algebraic_notation(current_position, move, False))
                self.moves_no_algebraic_notation.append(move)
            elif board[move[1]][move[0]].color != self.color:
                self.moves.append(self.an.get_rook_algebraic_notation(current_position, move, True))
                self.moves_no_algebraic_notation.append(move)
                break
            elif board[move[1]][move[0]].color == self.color:
                break
            
        return self.moves
            