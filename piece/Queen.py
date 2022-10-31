import os
import sys

from piece.Piece import Piece
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dir_path, os.pardir)))

from board.AlgebraicNotation import AlgebraicNotation

class Queen(Piece):
    def __init__(self, x, y, color, filename):
        super().__init__(x, y, color, filename)
        self.an = AlgebraicNotation()
        self.moves = []
        self.moves_no_algebraic_notation = []
        
    def get_moves(self, board):
        self.moves = []
        self.moves_no_algebraic_notation = []

        self.get_rook_moves(board)
        self.get_bishop_moves(board)
        
        return self.moves
    
    def get_bishop_moves(self, board):
        current_position = (self.x, self.y)

        bishop_diagonals = [[-1,-1], [1,-1], [-1,1], [1,1]]
        while len(bishop_diagonals) != 0:
            for diagonal in bishop_diagonals:
                move = (diagonal[0] + self.x, diagonal[1] + self.y)
                if move[0] >= 0 and move[0] <= 7 and move[1] >= 0 and move[1] <= 7:
                    if board[move[1]][move[0]] is None:
                        self.moves.append(self.an.get_queen_algebraic_notation(current_position, move, False))
                        self.moves_no_algebraic_notation.append(move)
                    elif board[move[1]][move[0]].color != self.color:
                        self.moves.append(self.an.get_queen_algebraic_notation(current_position, move, True))
                        self.moves_no_algebraic_notation.append(move)
                        bishop_diagonals.remove(diagonal)
                    elif board[move[1]][move[0]].color == self.color:
                        bishop_diagonals.remove(diagonal)
                else:
                    bishop_diagonals.remove(diagonal)
                    
                if diagonal:
                    if diagonal[0] > 0:
                        diagonal[0] += 1
                    else:
                        diagonal[0] -= 1 
                        
                    if diagonal[1] > 0:
                        diagonal[1] += 1
                    else:
                        diagonal[1] -= 1 
                        
    
    def get_rook_moves(self, board):
        current_position = (self.x, self.y)
        
        for x in range(self.x + 1, 8):
            move = (x, self.y)
            if board[move[1]][move[0]] is None:
                self.moves.append(self.an.get_queen_algebraic_notation(current_position, move, False))
                self.moves_no_algebraic_notation.append(move)
            elif board[move[1]][move[0]].color != self.color:
                self.moves.append(self.an.get_queen_algebraic_notation(current_position, move, True))
                self.moves_no_algebraic_notation.append(move)
                break
            elif board[move[1]][move[0]].color == self.color:
                break
            
        for x in range(self.x - 1, -1, -1):
            move = (x, self.y)
            if board[move[1]][move[0]] is None:
                self.moves.append(self.an.get_queen_algebraic_notation(current_position, move, False))
                self.moves_no_algebraic_notation.append(move)
            elif board[move[1]][move[0]].color != self.color:
                self.moves.append(self.an.get_queen_algebraic_notation(current_position, move, True))
                self.moves_no_algebraic_notation.append(move)
                break
            elif board[move[1]][move[0]].color == self.color:
                break
            
        for y in range(self.y + 1, 8):
            move = (self.x, y)
            if board[move[1]][move[0]] is None:
                self.moves.append(self.an.get_queen_algebraic_notation(current_position, move, False))
                self.moves_no_algebraic_notation.append(move)
            elif board[move[1]][move[0]].color != self.color:
                self.moves.append(self.an.get_queen_algebraic_notation(current_position, move, True))
                self.moves_no_algebraic_notation.append(move)
                break
            elif board[move[1]][move[0]].color == self.color:
                break
            
            
        for y in range(self.y - 1, -1, -1):
            move = (self.x, y)
            if board[move[1]][move[0]] is None:
                self.moves.append(self.an.get_queen_algebraic_notation(current_position, move, False))
                self.moves_no_algebraic_notation.append(move)
            elif board[move[1]][move[0]].color != self.color:
                self.moves.append(self.an.get_queen_algebraic_notation(current_position, move, True))
                self.moves_no_algebraic_notation.append(move)
                break
            elif board[move[1]][move[0]].color == self.color:
                break
        
        