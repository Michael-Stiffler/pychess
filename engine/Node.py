class Node():

    def __init__(self, board, pieces_on_board, root=None, move=None):
        self.root = root
        self.pieces_on_board = pieces_on_board
        self.board = board
        self.move = move
        self.children = []

    def set_children(self, children):
        self.children = children

    def get_children(self):
        return self.children

    def get_board(self):
        return self.board

    def get_pieces_on_board(self):
        return self.pieces_on_board
