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
        self._training_vectors = np.stack(training_vectors, axis=1)
        self._exp_output = np.stack(exp_output_vectors, axis=1)

        self._batch_size = training_batch_size
        self._num_batches = (len(training_vectors) + self._batch_size - 1) // self._batch_size
        self._input_batches = [None] * self._num_batches
        self._exp_output_batches = [None] * self._num_batches

        for i in range(self._num_batches):
            start = i * self._batch_size
            self._input_batches[i] = self._training_vectors[:, start:start + self._batch_size]
            self._exp_output_batches[i] = self._exp_output[:, start:start + self._batch_size]


    @staticmethod
    def sqr_diff_batch_cost(batch_output, exp_batch_output):
        return np.sum((batch_output - exp_batch_output) ** 2) / (2 * batch_output.shape[0])


    @staticmethod
    def sqr_diff_deriv_batch_cost(batch_output, exp_batch_output):
        return np.sum(batch_output - exp_batch_output, axis=1) / batch_output.shape[0]


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


    def train_model(self):
        # for i in range(len(self._input_batches) - 1):
        i = 0
        output = self._model.run_model(self._input_batches[i], Trainer.sigmoid)

        cost = Trainer.sqr_diff_batch_cost(
            output,
            self._exp_output_batches[i]
        )

        cost_deriv = Trainer.sqr_diff_deriv_batch_cost(
            output,
            self._exp_output_batches[i]
        )

        print(cost)
        print()
        print(cost_deriv)
