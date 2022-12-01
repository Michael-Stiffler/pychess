from board.AlgebraicNotation import *
import pickle
import os
import sys
import random
from engine.Node import Node
from multiprocessing import Pool


dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dir_path, os.pardir)))


class Engine():

    def __init__(self, board, depth):
        self.pieces_on_board = []
        self.current_board = [[]]
        self.moves_in_current_board = []
        self.nodes_to_look_at = []
        self.depth = depth
        self.board_obj = board
        self.root = None
        self.children = []

    def set_position(self):
        self.current_board = self.board_obj.get_board()

    def set_pieces_on_board(self):
        self.pieces_on_board = self.board_obj.get_pieces_on_board()

    def set_children(self, children):
        self.children.extend(children)

    def find_best_move(self):
        self.create_root_node()
        for _ in range(self.depth):
            self.board_obj.color_to_move = 1 if self.board_obj.color_to_move == 0 else 0
            for node in self.nodes_to_look_at:
                self.process_current_child(node)
            self.nodes_to_look_at = []
            self.nodes_to_look_at = self.children
            self.children = []

        if self.depth % 2 != 0:
            self.board_obj.color_to_move = 1 if self.board_obj.color_to_move == 0 else 0

        move = self.root.get_children()[0].move

        node = random.choice(self.root.get_children())
        move = node.move
        for piece in self.pieces_on_board:
            if move in piece.get_moves():
                return move, piece

    def process_current_child(self, node):
        self.board_obj.get_piece_moves(
            board=node.get_board(), pieces_on_board=node.get_pieces_on_board())
        moves = self.board_obj.get_moves()
        self.set_children(self.create_children_nodes(node, moves))

    def create_root_node(self):
        self.root = Node(board=self.current_board,
                         pieces_on_board=self.pieces_on_board)
        self.board_obj.get_piece_moves(
            board=self.root.board, pieces_on_board=self.root.pieces_on_board)
        moves = self.board_obj.get_moves()
        children = self.create_children_nodes(self.root, moves)
        self.root.set_children(children)
        self.nodes_to_look_at = children

    def create_children_nodes(self, node, moves):
        children = []

        for move in moves:
            node_board = pickle.loads(pickle.dumps(node.get_board(), -1))
            node_pieces_on_board = pickle.loads(pickle.dumps(node.get_pieces_on_board(), -1))
            self.board_obj.set_copy_pieces_on_board(node_pieces_on_board)
            self.board_obj.set_copy_board(node_board)
            for piece in node_pieces_on_board:
                if move in piece.get_moves():
                    self.board_obj.make_move(move, piece, node_board, node_pieces_on_board)
                    board = pickle.loads(pickle.dumps(self.board_obj.get_copy_board(), -1))
                    pieces_on_board = pickle.loads(pickle.dumps(self.board_obj.get_copy_pieces_on_board(), -1))
                    children.append(Node(move=move, board=board, pieces_on_board=pieces_on_board, root=node))
                    break

        return children

    def reset_tree(self):
        self.pieces_on_board = []
        self.current_board = [[]]
        self.moves_in_current_board = []
        self.nodes_to_look_at = []
        self.root = None
        self.children = []

    if __name__ == "__main__":
        pass
