import json
import pickle
import os 
import sys
from engine.Node import Node
import ujson
import ast


dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dir_path, os.pardir)))

from board.AlgebraicNotation import AlgebraicNotation

class Engine():
    
    def __init__(self, board, depth):
        self.pieces_on_board = []
        self.current_board = [[]]
        self.moves_in_current_board = []
        self.nodes_to_look_at = []
        self.depth = depth
        self.board_obj = board
        self.an = AlgebraicNotation()
        self.root = None
    
    def set_position(self):
        self.current_board = self.board_obj.get_board()
        
    def set_moves(self):
        self.moves_in_current_board = self.board_obj.get_moves()
    
    def set_pieces_on_board(self):
        self.pieces_on_board = self.board_obj.get_pieces_on_board()
        
    def find_best_move(self):
        self.create_root_node()
        count = 0
        for x in range(self.depth):
            new_children = []
            self.board_obj.color_to_move = 1 if self.board_obj.color_to_move == 0 else 0
            for node in self.nodes_to_look_at:
                self.board_obj.get_piece_moves(board=node.get_board(), pieces_on_board=node.get_pieces_on_board())
                self.set_moves()
                new_children.extend(self.create_children_nodes(node))
                count +=1
            self.nodes_to_look_at = new_children
        print(count)
        self.board_obj.color_to_move = 1 if self.board_obj.color_to_move == 0 else 0
        move = self.root.get_children()[0].move
        for piece in self.pieces_on_board:
            if move in piece.get_moves():
                return move, piece
       
    def create_root_node(self):
        self.root = Node(board=self.current_board, pieces_on_board=self.pieces_on_board)
        children = self.create_children_nodes(self.root)
        self.root.set_children(children)
        self.nodes_to_look_at = children
        
    def create_children_nodes(self, node):
        children = []
        
        for move in self.moves_in_current_board:
            node_board = pickle.loads(pickle.dumps(node.get_board(), -1))
            node_pieces_on_board = pickle.loads(pickle.dumps(node.get_pieces_on_board(), -1))
            self.board_obj.set_copy_pieces_on_board(node_pieces_on_board)
            self.board_obj.set_copy_board(node_board)
            for piece in node_pieces_on_board:
                if move in piece.get_moves():
                    self.board_obj.make_move(move, piece, node_board, node_pieces_on_board)
                    #board = pickle.loads(pickle.dumps(self.board_obj.get_copy_board(), -1))
                    board = self.board_obj.get_copy_board()
                    #pieces_on_board = pickle.loads(pickle.dumps(self.board_obj.get_copy_pieces_on_board(), -1))
                    pieces_on_board = self.board_obj.get_copy_pieces_on_board()
                    children.append(Node(move=move, board=board, pieces_on_board=pieces_on_board, root=node))
                    break  
                  
        return children


