import chess

infile = open("moves.tsv", 'r')
outfile = open('openings.epd', 'w')

for line in infile:
    line = line[:-1].split('\t')[2].split(' ')
    board = chess.Board()
    for l in line:
        if '.' not in l:
            m = board.parse_san(l)
            board.push(m)
    outfile.write(board.fen() + '\n')
