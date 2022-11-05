from abc import abstractmethod

class Piece():
    def __init__(self, x=0, y=0, color=0, filename=''):
        self.x = x
        self.y = y
        self.color = color
        self.filename = filename
        self.WHITE = 0
        self.BLACK = 1
    
    @abstractmethod
    def get_moves(self):
        pass
    
    @abstractmethod
    def get_moves_no_algebraic_notation(self):
        pass
    
    @abstractmethod
    def calculate_moves(self):
        pass
    
    @abstractmethod
    def reset_moves(self):
        pass
    
    def promote_to_queen():
        pass
    
    def promote_to_rook():
        pass
    
    def promote_to_bishop():
        pass
    
    def promote_to_knight():
        pass


        