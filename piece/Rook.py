from board.AlgebraicNotation import *
import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dir_path, os.pardir)))


class Rook():
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
        self.moves.clear()
        self.moves_no_algebraic_notation.clear()
        current_position = (self.x, self.y)

        for x in range(self.x + 1, 8):
            move = (x, self.y)
            if board[move[1]][move[0]] is None:
                self.moves.append(get_rook_algebraic_notation(
                    current_position, move, False))
                self.moves_no_algebraic_notation.append(move)
            elif board[move[1]][move[0]].color != self.color:
                self.moves.append(get_rook_algebraic_notation(
                    current_position, move, True))
                self.moves_no_algebraic_notation.append(move)
                break
            elif board[move[1]][move[0]].color == self.color:
                break

        for x in range(self.x - 1, -1, -1):
            move = (x, self.y)
            if board[move[1]][move[0]] is None:
                self.moves.append(get_rook_algebraic_notation(
                    current_position, move, False))
                self.moves_no_algebraic_notation.append(move)
            elif board[move[1]][move[0]].color != self.color:
                self.moves.append(get_rook_algebraic_notation(
                    current_position, move, True))
                self.moves_no_algebraic_notation.append(move)
                break
            elif board[move[1]][move[0]].color == self.color:
                break

        for y in range(self.y + 1, 8):
            move = (self.x, y)
            if board[move[1]][move[0]] is None:
                self.moves.append(get_rook_algebraic_notation(
                    current_position, move, False))
                self.moves_no_algebraic_notation.append(move)
            elif board[move[1]][move[0]].color != self.color:
                self.moves.append(get_rook_algebraic_notation(
                    current_position, move, True))
                self.moves_no_algebraic_notation.append(move)
                break
            elif board[move[1]][move[0]].color == self.color:
                break

        for y in range(self.y - 1, -1, -1):
            move = (self.x, y)
            if board[move[1]][move[0]] is None:
                self.moves.append(get_rook_algebraic_notation(
                    current_position, move, False))
                self.moves_no_algebraic_notation.append(move)
            elif board[move[1]][move[0]].color != self.color:
                self.moves.append(get_rook_algebraic_notation(
                    current_position, move, True))
                self.moves_no_algebraic_notation.append(move)
                break
            elif board[move[1]][move[0]].color == self.color:
                break

    def get_moves_no_algebraic_notation(self):
        return self.moves_no_algebraic_notation

    def get_moves(self):
        return self.moves

    def reset_moves(self):
        self.moves = []
        self.moves_no_algebraic_notation = []

    def encode(self):
        return self.__dict__
