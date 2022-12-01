files = [1, 2, 3, 4, 5, 6, 7, 8]
ranks = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']


def get_pawn_promotion_notation(start, end, is_capture):
    if not is_capture:
        return f"{get_rank_letter(end[0])}{get_file_number(end[1])}=Q"
    else:
        return f"{get_rank_letter(start[0])}x{get_rank_letter(end[0])}{get_file_number(end[1])}=Q"


def get_pawn_algebraic_notation(start, end, is_capture):
    if not is_capture:
        return f"{get_rank_letter(end[0])}{get_file_number(end[1])}"
    else:
        return f"{get_rank_letter(start[0])}x{get_rank_letter(end[0])}{get_file_number(end[1])}"


def get_knight_algebraic_notation(start, end, is_capture):
    if not is_capture:
        return f"N{get_rank_letter(end[0])}{get_file_number(end[1])}"
    else:
        return f"Nx{get_rank_letter(end[0])}{get_file_number(end[1])}"


def get_bishop_algebraic_notation(start, end, is_capture):
    if not is_capture:
        return f"B{get_rank_letter(end[0])}{get_file_number(end[1])}"
    else:
        return f"Bx{get_rank_letter(end[0])}{get_file_number(end[1])}"


def get_queen_algebraic_notation(start, end, is_capture):
    if not is_capture:
        return f"Q{get_rank_letter(end[0])}{get_file_number(end[1])}"
    else:
        return f"Qx{get_rank_letter(end[0])}{get_file_number(end[1])}"


def get_rook_algebraic_notation(start, end, is_capture):
    if not is_capture:
        return f"R{get_rank_letter(end[0])}{get_file_number(end[1])}"
    else:
        return f"Rx{get_rank_letter(end[0])}{get_file_number(end[1])}"


def get_king_algebraic_notation(start, end, is_capture):
    if not is_capture:
        return f"K{get_rank_letter(end[0])}{get_file_number(end[1])}"
    else:
        return f"Kx{get_rank_letter(end[0])}{get_file_number(end[1])}"


def get_king_castle_notation(kingside):
    if kingside:
        return f"O-O"
    else:
        return f"O-O-O"


def get_rank_letter(num):
    return ranks[num]


def get_file_number(num):
    return files[-(num + 1)]


def get_square_from_algebraic_notation(move):
    if move[-1].isnumeric():
        square = move[-2:]
        return (ranks.index(square[0]), files[(-int(square[1]))] - 1)
    if move[-1] in "$#+":
        if move[-3] == "=":
            square = move[-5:-3]
            return (ranks.index(square[0]), files[(-int(square[1]))] - 1)
        else:
            square = move[-3:-1]
            return (ranks.index(square[0]), files[(-int(square[1]))] - 1)
    if move[2] == "=" or move[-2] == "=":
        square = move[-4:-2]
        return (ranks.index(square[0]), files[(-int(square[1]))] - 1)


def get_castle_square_from_algebraic_notation(move, piece):
    if move == "O-O":
        if piece.color == 0:
            return (6, 7)
        else:
            return (6, 0)
    else:
        if piece.color == 0:
            return (2, 7)
        else:
            return (2, 0)


def encode():
    return __dict__
