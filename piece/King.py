from board.AlgebraicNotation import *
import os
import sys

from piece.Rook import Rook
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dir_path, os.pardir)))


class King():
    def __init__(self, x, y, color, filename):
        self.moves = []
        self.moves_no_algebraic_notation = []
        self.can_castle_kingside = True
        self.can_castle_queenside = True
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

        if self.can_castle_kingside:
            if self.color == self.WHITE:
                if current_position == (4, 7) and isinstance(board[7][7], Rook):
                    if board[7][5] is None and board[7][6] is None:
                        self.moves.append(
                            get_king_castle_notation(True))
                        self.moves_no_algebraic_notation.append((6, 7))
                else:
                    self.can_castle_kingside = False
            elif self.color == self.BLACK:
                if current_position == (4, 0) and isinstance(board[0][7], Rook):
                    if board[0][5] is None and board[0][6] is None:
                        self.moves.append(
                            get_king_castle_notation(True))
                        self.moves_no_algebraic_notation.append((6, 0))
                else:
                    self.can_castle_kingside = False
        if self.can_castle_queenside:
            if self.color == self.WHITE:
                if current_position == (4, 7) and isinstance(board[7][0], Rook):
                    if board[7][3] is None and board[7][2] is None and board[7][1] is None:
                        self.moves.append(
                            get_king_castle_notation(False))
                        self.moves_no_algebraic_notation.append((2, 7))
                else:
                    self.can_castle_queenside = False
            elif self.color == self.BLACK:
                if current_position == (4, 0) and isinstance(board[0][0], Rook):
                    if board[0][3] is None and board[0][2] is None and board[0][1] is None:
                        self.moves.append(
                            get_king_castle_notation(False))
                        self.moves_no_algebraic_notation.append((2, 0))
                else:
                    self.can_castle_queenside = False

        for x in range(-1, 2):
            for y in range(-1, 2):
                if x == 0 and y == 0:
                    continue
                move = (self.x+x, self.y+y)
                if move[0] >= 0 and move[0] <= 7 and move[1] >= 0 and move[1] <= 7:
                    if board[move[1]][move[0]] is None:
                        self.moves.append(get_king_algebraic_notation(
                            current_position, move, False))
                        self.moves_no_algebraic_notation.append(move)
                    elif board[move[1]][move[0]].color != self.color:
                        self.moves.append(get_king_algebraic_notation(
                            current_position, move, True))
                        self.moves_no_algebraic_notation.append(move)

    def get_moves_no_algebraic_notation(self):
        return self.moves_no_algebraic_notation

    def get_moves(self):
        return self.moves

    def reset_moves(self):
        self.moves = []

    def reset_moves(self):
        self.moves = []
        self.moves_no_algebraic_notation = []

    def encode(self):
        return self.__dict__
