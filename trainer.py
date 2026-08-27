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


    def train_model(self, epoch_count):
        epoch_count_digits = int(np.floor(np.log10(epoch_count) + 1))

        # for i in range(1, epoch_count + 1):
        # for j in range(len(self._input_batches) - 1):
        i = 1
        j = 0
        output = self._model.run_model(self._input_batches[j], Trainer.sigmoid)
        cost_func = Trainer.sqr_diff_batch_cost

        self._backpropagate(
            output, self._exp_output_batches[j],
            Trainer.sqr_diff_deriv_batch_cost,
            Trainer.sigmoid_deriv
        )

        cost = cost_func(output, self._exp_output_batches[j])
        print(f"Epoch {i:0(epoch_count_digits)d}: cost = {cost:.6f}")


    def _backpropagate(self,
        output_batch, expected_output_batch,
        cost_deriv_func,
        norm_deriv_func,
        learning_rate=1.0):
        norm_lyr_outp = self._model.norm_lyr_output
        pre_norm_lyr_outp = self._model.pre_norm_lyr_output
        lyr_count = self._model.layer_count
        product = cost_deriv_func(output_batch, expected_output_batch)

        for i in range(lyr_count - 1, 0, -1):
            product *= norm_deriv_func(output_batch)
            bias_deriv = product
            wght_deriv = product * pre_norm_lyr_outp[i]
