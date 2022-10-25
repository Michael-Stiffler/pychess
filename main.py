import sys
import time
import pygame as py
import math
from board.Board import Board

def main():
    running = True
    need_to_calculate_moves = True
    py.init()
    #board = Board(py.display.set_mode((800, 800)), 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
    #board = Board(py.display.set_mode((800, 800)), "2kr3r/p1ppqpb1/bn2Qnp1/3PN3/1p2P3/2N5/PPPBBPPP/R3K2R b KQ - 3 2")
    board = Board(display=py.display.set_mode((800, 800)), fen="rn1q1rk1/ppp2ppp/4pn2/3p4/1b1P4/N1N1P1P1/PPPB1PBP/R2QKbR1 b Q - 8 9")

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
            elif event.type == py.MOUSEBUTTONUP:
                pos_on_mouse_up = py.mouse.get_pos()
                pos_on_mouse_up_square = (math.floor(pos_on_mouse_up[0] / board.SIZE), math.floor(pos_on_mouse_up[1] / board.SIZE))
                print(pos_on_mouse_up_square) 
                    
                if pos_on_mouse_up_square != pos_on_mouse_down_square:
                    move = board.check_user_move(pos_on_mouse_down_square, pos_on_mouse_up_square)
                    if move:
                        board.make_move(move)
                    
                board.draw_board()
                board.draw_pieces()
                need_to_calculate_moves = True


        py.display.flip()
        py.display.update()

if __name__ == '__main__':
    main()
