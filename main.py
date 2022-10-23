import sys
import pygame as py
import math
from board.Board import Board

py.init()
board = Board(py.display.set_mode((800, 800)), 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')

def main():
    running = True
    board.load_pieces()
    board.draw_board()
    board.draw_pieces()
    board.initialize_show_square()
    
    while running:        
        board.show_square(py.mouse.get_pos())

        for event in py.event.get():
            if event.type == py.QUIT:
                running = False
                sys.exit()
            # elif event.type == py.MOUSEBUTTONDOWN:
            #     previousPos = py.mouse.get_pos()
            #     previousPos = (math.floor(previousPos[0]), math.floor(previousPos[1]))
            #     print(previousPos)
            #     # engine.getPiece(previousPos[0] / squareSize, previousPos[1] / squareSize)
            # elif event.type == py.MOUSEBUTTONUP:
            #     currentPos = py.mouse.get_pos()
            #     currentPos = (math.floor(currentPos[0]), math.floor(currentPos[1]))
            #     if currentPos == previousPos:
            #         break
            #     # engine.movePiece(currentPos[0] / squareSize, currentPos[1] / squareSize)
            #     board.drawBoard()
            #     board.drawPieces()

        py.display.flip()
        py.display.update()

if __name__ == '__main__':
    main()
