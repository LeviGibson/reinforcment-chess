import chess
import tensorflow as tf
import keras
from keras.layers import Dense
import halfkp
import labels
import numpy as np

RELU = 'relu'
SIGMOID = 'sigmoid'


class ReinforcmentLearningNet:
    def __init__(self, layer_sizes, activations, loss='mse', modelPath = None):
        if modelPath != None:
            self.model = keras.models.load_model(modelPath)
        else:
            self.model = keras.models.Sequential()
            self.model.add(Dense(layer_sizes[0], activation=activations[0], input_shape=(98304,)))

            for activation, size in zip(activations[1:], layer_sizes[1:]):
                self.model.add(Dense(size, activation=activation))

            tf.keras.utils.plot_model(self.model, show_shapes=True, show_layer_names=True, to_file='model.png')
            self.model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.1), loss=loss, metrics=['mae'])

    def fit(self, moves, weight: float, fens):
        x = []
        y = []
        for move, fen in zip(moves, fens):
            board = chess.Board(fen)
            x.append(halfkp.get_halfkp_indeicies(board)[0])
            i1, i2 = labels.move_to_index(move, board)
            y.append(np.zeros((128,)) + 0.5)
            y[-1][i1] = weight
            y[-1][i2] = weight

        x = np.array(x)
        y = np.array(y)
        self.model.fit(x, y, batch_size=1)

    def predict(self, board: chess.Board, randomness):
        indices = halfkp.get_halfkp_indeicies(board)
        networkOutput = self.model.predict(indices)
        networkOutput *= np.random.random_sample(networkOutput.shape)
        networkOutput = networkOutput.reshape((2, 64))



        legalMoves = list(board.legal_moves)
        maxEval = -1
        maxMove = legalMoves[0]

        for legalMoveCount, move in enumerate(legalMoves):
                board.push(move)
                if board.can_claim_threefold_repetition():
                    board.pop()
                    continue
                if board.is_checkmate():
                    board.pop()
                    return move
                board.pop()

                i1, i2 = labels.move_to_index(move, board)
                score = networkOutput[0][i1] * networkOutput[1][i2]
                if score > maxEval:
                    maxEval = score
                    maxMove = move

            return maxMove

if __name__ == '__main__':
    r = ReinforcmentLearningNet([512, 128],
                                [RELU, RELU, SIGMOID])
