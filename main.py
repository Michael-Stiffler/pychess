from board.AlgebraicNotation import AlgebraicNotation
import sys
import pygame as py
from board.Board import Board
from board.DrawBoard import DrawBoard
from engine.Engine import Engine
import cProfile
import pstats
import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dir_path, os.pardir)))


def main():
    py.init()

    #board = Board(display=py.display.set_mode((800, 800)), fen='2r3r1/4N3/RN6/8/8/7Q/R7/5Q2 w - - 0 1')
    board = Board(
        fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
    #board = Board(fen='2kr3r/p1ppqpb1/bn2Qnp1/3PN3/1p2P3/2N5/PPPBBPPP/R3K2R b KQ - 3 2')
    #board = Board(fen='rn1q1rk1/ppp2ppp/4pn2/3p4/1b1P4/N1N1P1P1/PPPB1PBP/R2QKbR1 b Q - 8 9')
    #board = Board(fen='r1bqkb1r/pp1ppppp/2p2n2/5n2/P1B2N2/4PN2/1PPP1PPP/R1BQK2R w kq - 1 10')
    #board = Board(fen='5k2/2p2b2/8/3P4/2K5/8/8/8 b - - 0 1')
    #board = Board(fen='5k2/1Q6/5K2/8/8/8/8/8 w - - 0 1')

    db = DrawBoard(display=py.display.set_mode((800, 800)))
    engine = Engine(board=board, depth=2)
    an = AlgebraicNotation()

    running = True
    need_to_calculate_moves = True
    holding_piece = False
    user_color = 0
    clock = py.time.Clock()

    board.parse_fen()
    db.load_pieces()
    db.draw_board()
    db.draw_pieces(board.get_board())
    db.initialize_show_square()

    while running:
        mouse_pos = py.mouse.get_pos()
        db.show_square(mouse_pos)

        if need_to_calculate_moves:
            with cProfile.Profile() as pr:
                board.get_piece_moves()
                # if not board.white_to_move():
                #     engine.set_position()
                #     engine.set_pieces_on_board()
                #     move, piece = engine.find_best_move()
                #     board.make_move(move, piece)
                #     board.switch_color_to_move()
                #     db.draw_board()
                #     db.draw_pieces(board.get_board())
                #     board.get_piece_moves()
                #     engine.reset_tree()

            # stats = pstats.Stats(pr)
            # stats.sort_stats(pstats.SortKey.TIME)
            # stats.print_stats()

            need_to_calculate_moves = False

        if holding_piece:
            db.draw_board()
            db.draw_moves()
            db.drag_piece(mouse_pos, board.get_board())

        for event in py.event.get():
            if event.type == py.QUIT:
                running = False
                sys.exit()
            elif event.type == py.MOUSEBUTTONDOWN:
                square_pos_on_mouse_down = board.get_square_from_mouse_pos(
                    mouse_pos)
                print(square_pos_on_mouse_down)
                piece = board.return_piece_on_square(square_pos_on_mouse_down)
                if piece and piece.color == board.color_to_move:
                    db.piece_held = piece
                    holding_piece = True
            elif event.type == py.MOUSEBUTTONUP:
                square_pos_on_mouse_up = board.get_square_from_mouse_pos(
                    mouse_pos)
                print(square_pos_on_mouse_up)
                if square_pos_on_mouse_down != square_pos_on_mouse_up:
                    move = board.check_user_move(
                        square_pos_on_mouse_down, square_pos_on_mouse_up)
                    if move:
                        piece = board.return_piece_on_square(
                            square_pos_on_mouse_down)
                        board.make_move(move, piece)
                        board.switch_color_to_move()
                        need_to_calculate_moves = True
                db.draw_board()
                db.draw_pieces(board.get_board())
                holding_piece = False

        py.display.flip()
        py.display.update()

        clock.tick(60)
        # print(clock.get_fps())


if __name__ == '__main__':
    main()
