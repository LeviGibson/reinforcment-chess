import chess

from network import *
import chess.pgn
import chess.syzygy

WHITE_WIN = 1
BLACK_WIN = 0
DRAW = 0.5


class NnomTrainer:
    def __init__(self, syzygyPath, modelPath=None):
        self.net = ReinforcmentLearningNet([512, 128], [RELU, SIGMOID], modelPath=modelPath)
        self.syzygy = chess.syzygy.open_tablebase(syzygyPath)

    def play_game(self):
        gameResult = DRAW
        board = chess.Board()
        fens = [[], []]
        moves = [[], []]

        while not board.is_game_over():
            predmove = self.net.predict(board, 0.2)
            print(predmove, end=' ')

            fens[board.turn].append(board.fen())
            moves[board.turn].append(predmove)

            board.push(predmove)

            try:
                tbres = syzygy.probe_wdl(board)
                if tbres != 0:
                    if tbres > 0:
                        return WHITE_WIN if board.turn == chess.WHITE else BLACK_WIN
                    if tbres < 0:
                        return WHITE_WIN if board.turn == chess.BLACK else BLACK_WIN
            except:
                pass

            if board.is_checkmate():
                if board.turn == chess.BLACK:
                    gameResult = WHITE_WIN
                else:
                    gameResult = BLACK_WIN

        print()

        if gameResult == BLACK_WIN:
            fens[0], fens[1] = fens[1], fens[0]
            moves[0], moves[1] = moves[1], moves[0]

        if gameResult != DRAW:
            self.net.fit(moves[0], 1, fens[0])
            self.net.fit(moves[1], 0, fens[1])


    def train(self, iters):
        for i in range(iters):
            if i % 10 == 0:
                self.net.model.save("network")
            self.play_game()
