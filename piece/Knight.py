from board.AlgebraicNotation import *
import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dir_path, os.pardir)))


class Knight():
    def __init__(self, x, y, color, filename):
        self.moves = []
        self.moves_no_algebraic_notation = []
        self.x = x
        self.y = y
        self.color = color
        self.filename = filename
        self.WHITE = 0
        self.BLACK = 1

    def calculate_moves(self, board):
        self.moves = []
        self.moves_no_algebraic_notation = []
        current_position = (self.x, self.y)

        knight_moves = [(self.x-1, self.y-2), (self.x+1, self.y-2), (self.x+2, self.y-1), (self.x+2, self.y+1),
                        (self.x-1, self.y+2), (self.x+1, self.y+2), (self.x-2, self.y-1), (self.x-2, self.y+1)]

        for move in knight_moves:
            if move[0] >= 0 and move[0] <= 7 and move[1] >= 0 and move[1] <= 7:
                if board[move[1]][move[0]] is None:
                    self.moves.append(get_knight_algebraic_notation(
                        current_position, move, False))
                    self.moves_no_algebraic_notation.append(move)
                elif board[move[1]][move[0]].color != self.color:
                    self.moves.append(get_knight_algebraic_notation(
                        current_position, move, True))
                    self.moves_no_algebraic_notation.append(move)

    def get_moves_no_algebraic_notation(self):
        return self.moves_no_algebraic_notation

    def get_moves(self):
        return self.moves

    def reset_moves(self):
        self.moves = []
        self.moves_no_algebraic_notation = []

    def encode(self):
        return self.__dict__
