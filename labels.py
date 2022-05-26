import chess

WHITE_PIECES = ['P', 'N', 'B', 'R', 'Q', 'K']
FLIP_PERS = [56, 57, 58, 59, 60, 61, 62, 63,
  48, 49, 50, 51, 52, 53, 54, 55,
  40, 41, 42, 43, 44, 45, 46, 47,
  32, 33, 34, 35, 36, 37, 38, 39,
  24, 25, 26, 27, 28, 29, 30, 31,
  16, 17, 18, 19, 20, 21, 22, 23,
  8, 9, 10, 11, 12, 13, 14, 15,
  0, 1, 2, 3, 4, 5, 6, 7]

def move_to_index(move : chess.Move, board : chess.Board):
    piece = board.piece_at(move.from_square)
    color = str(piece) in WHITE_PIECES
    piece = WHITE_PIECES.index(str(piece).upper())

    frsq = move.from_square
    tosq = move.to_square

    if color is chess.BLACK:
        frsq = FLIP_PERS[frsq]
        tosq = FLIP_PERS[tosq]

    return frsq, tosq

def index_to_move(i1, i2, board : chess.Board):
    if board.turn == chess.BLACK:
        i1, i2 = FLIP_PERS[i1], FLIP_PERS[i2]

    move = None
    lm = list(board.legal_moves)
    for m in lm:
        if m.from_square == i1 and m.to_square == i2:
            move = m

    return move
