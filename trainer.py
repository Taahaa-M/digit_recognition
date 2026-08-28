import numpy as np

from model import Model
from digit import Digits

class Trainer():
    # TODO: Store training progress in files
    def __init__(
        self,
        model,
        training_vectors,
        exp_output_vectors,
        training_batch_size=64
    ):
        self._model = model

        # use axis=1 so inputs are column vectors (stick to mathematical convention)
        self._training_vectors = np.concatenate(training_vectors, axis=1)
        self._exp_output = np.concatenate(exp_output_vectors, axis=1)
        self._batch_size = training_batch_size

        self._num_batches = (len(self._training_vectors) + self._batch_size - 1) // self._batch_size

        self._input_batches = [None] * self._num_batches
        self._exp_output_batches = [None] * self._num_batches

        self._shuffle_data()


    @staticmethod
    def sqr_diff_batch_cost(batch_output, exp_batch_output):
        return np.sum((batch_output - exp_batch_output) ** 2) / (2 * batch_output.shape[0])


    @staticmethod
    def sqr_diff_deriv_batch_cost(batch_output, exp_batch_output):
        return (batch_output - exp_batch_output) / batch_output.shape[0]


    @staticmethod
    def relu(x):
        return np.maximum(0, x)


    @staticmethod
    def relu_deriv(x):
        return x * (x > 0.0)


    @staticmethod
    def sigmoid(x):
        return 1.0 / (1.0 + np.exp(-x))


    @staticmethod
    def sigmoid_deriv(x):
        return 1.0 / (2.0 + np.exp(x) + np.exp(-x))


    def train_model(self, epoch_count, learning_rate=1.0):
        for i in range(1, epoch_count + 1):
            for j in range(len(self._input_batches) - 1):
                output = self._model.run_model(self._input_batches[j], Trainer.sigmoid)
                cost_func = Trainer.sqr_diff_batch_cost
                print(cost_func(output, self._exp_output_batches[j]))

                self._backpropagate(
                    output, self._exp_output_batches[j],
                    Trainer.sqr_diff_deriv_batch_cost,
                    Trainer.sigmoid_deriv,
                    learning_rate
                )
            self._shuffle_data()



    def _backpropagate(self,
        output_batch, expected_output_batch,
        cost_deriv_func,
        norm_deriv_func,
        learning_rate):
        z = self._model.pre_norm_lyr_output
        L = self._model.layer_count

        cum_deriv = cost_deriv_func(output_batch, expected_output_batch)

        for i in range(L - 1, 0, -1):
            batch_len = output_batch.shape[1]

            wght_mat = self._model.layers[i][Model.WGHT_MATRIX]
            bias_vec = self._model.layers[i][Model.BIAS_VEC]

            cum_deriv *= norm_deriv_func(z[i])

            bias_deriv = np.sum(cum_deriv, axis=1, keepdims=True) / batch_len  # dC/db = 1
            wght_deriv = cum_deriv @ z[i-1].T / batch_len
            
            cum_deriv = wght_mat.T @ cum_deriv

            wght_mat -= learning_rate * wght_deriv
            bias_vec -= learning_rate * bias_deriv


    def test(self, test_inputs, test_exp_outputs):
        total_inputs = len(test_inputs)
        success = 0
        for i, inp in enumerate(test_inputs):
            output = self._model.run_model(inp, Trainer.sigmoid)
            if (np.argmax(output) == np.argmax(test_exp_outputs[i])): success += 1


        print(f"Success rate: {100 * success / total_inputs:.6f}%")


    def _shuffle_data(self):
        shuffled_indices = np.random.permutation(self._training_vectors.shape[1])

        self._training_vectors = self._training_vectors[:, shuffled_indices]
        self._exp_output = self._exp_output[:, shuffled_indices]

        for i in range(self._num_batches):
            start = i * self._batch_size
            self._input_batches[i] = self._training_vectors[:, start:start + self._batch_size]
            self._exp_output_batches[i] = self._exp_output[:, start:start + self._batch_size]
