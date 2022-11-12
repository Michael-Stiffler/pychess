import pickle
import os 
import sys
from engine.Node import Node

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dir_path, os.pardir)))

from board.AlgebraicNotation import AlgebraicNotation

class Engine():
    
    def __init__(self, board, depth):
        self.pieces_on_board = []
        self.current_board = [[None for i in range(8)] for j in range(8)]
        self.moves_in_current_board = []
        self.depth = depth
        self.board_obj = board
        self.an = AlgebraicNotation()
        self.root = None
    
    def set_position(self):
        self.current_board = pickle.loads(pickle.dumps(self.board_obj.get_board(), -1))
        
    def set_moves(self):
        self.moves_in_current_board = self.board_obj.get_moves()
    
    def set_pieces_on_board(self):
        self.pieces_on_board = self.board_obj.get_pieces_on_board()
        
    def find_best_move(self):
        self.create_nodes()
        
    def create_nodes(self):
        if not self.root:
            children = []
            for move in self.moves_in_current_board:
                self.board_obj.set_copy_pieces_on_board(self.pieces_on_board)
                pieces_on_board = self.board_obj.get_copy_pieces_on_board()
                self.board_obj.set_copy_board(self.current_board)
                board = self.board_obj.get_copy_board()
                piece = self.board_obj.return_piece_on_square(self.an.get_square_from_algebraic_notation(move), board)
                self.board_obj.make_move(move, piece, board, pieces_on_board)
                board = self.board_obj.get_copy_board()
                children.append(Node(board=board, children=[]))
            self.root = Node(board=self.current_board, children=children)

