

from abc import abstractmethod


class Piece():
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        
    @abstractmethod
    def get_moves():
        pass
    
    def make_move():
        pass
    
    def promote_to_queen():
        pass
    
    def promote_to_rook():
        pass
    
    def promote_to_bishop():
        pass
    
    def promote_to_knight():
        pass
        