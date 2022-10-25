import sys
import time
import pygame as py
import math
from board.Board import Board

def main():
    running = True
    need_to_calculate_moves = True
    py.init()
    board = Board(py.display.set_mode((800, 800)), 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
    #board = Board(py.display.set_mode((800, 800)), "2kr3r/p1ppqpb1/bn2Qnp1/3PN3/1p2P3/2N5/PPPBBPPP/R3K2R b KQ - 3 2")
    
    board.parse_fen()
    board.load_pieces()
    board.draw_board()
    board.draw_pieces()
    board.initialize_show_square()
    
    while running:  
        if need_to_calculate_moves:
            board.get_piece_moves()   
            need_to_calculate_moves = False   

        board.show_square(py.mouse.get_pos())

        for event in py.event.get():
            if event.type == py.QUIT:
                running = False
                sys.exit()
            elif event.type == py.MOUSEBUTTONDOWN:
                pos_on_mouse_down = py.mouse.get_pos()
                pos_on_mouse_down_square = (math.floor(pos_on_mouse_down[0] / board.SIZE), math.floor(pos_on_mouse_down[1] / board.SIZE))
                print(pos_on_mouse_down_square)
            #   engine.getPiece(previousPos[0] / squareSize, previousPos[1] / squareSize)
            elif event.type == py.MOUSEBUTTONUP:
                pos_on_mouse_up = py.mouse.get_pos()
                pos_on_mouse_up_square = (math.floor(pos_on_mouse_up[0] / board.SIZE), math.floor(pos_on_mouse_up[1] / board.SIZE))
                print(pos_on_mouse_up_square)     
                if pos_on_mouse_up_square == pos_on_mouse_down_square:
                    print("same square")
                need_to_calculate_moves = True
            #     # engine.movePiece(currentPos[0] / squareSize, currentPos[1] / squareSize)
            #     board.drawBoard()
            #     board.drawPieces()

        py.display.flip()
        py.display.update()

if __name__ == '__main__':
    main()
