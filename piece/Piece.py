from abc import abstractmethod

class Piece():
    def __init__(self, x, y, color, filename):
        self.x = x
        self.y = y
        self.color = color
        self.filename = filename
        
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
        