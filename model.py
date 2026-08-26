import sys
import numpy as np


class Model():
    # indices for layer indexing
    WGHT_MATRIX = 0
    BIAS_VEC = 1
    # TODO: Store and load model from file
    # neuron_count_list describes the number of neurons in each layer from start to end
    def __init__(self, input_size, output_size, neuron_count_list):
        try:
            assert(neuron_count_list[0] == input_size)
            assert(neuron_count_list[-1] == output_size)
        except:
            print("neuron_count_list[0] must be the same as input_size", file=sys.stderr)
            print("neuron_count_list[-1] must be the same as output_size", file=sys.stderr)
            quit()

        self.layers = []
        self.layer_count = len(neuron_count_list)

        for i in range(1, self.layer_count):
            lyr_input_size = neuron_count_list[i-1]
            lyr_output_size = neuron_count_list[i]

            self.layers.append([
                np.random.default_rng().normal(  # weight matrix
                    0.0,
                    np.sqrt(2.0 / lyr_input_size),
                    size=(lyr_output_size, lyr_input_size),
                ),
                np.zeros(                        # bias vector
                    lyr_output_size,
                    dtype=np.float64
                )
            ])


    def _get_cost(self, output, expected_output):  # vectors of same size
        pass


    def _backpropagate(self):
        pass


    def run_model(self, input):
        for lyr in self.layers:
            input = lyr[Model.WGHT_MATRIX] @ input + lyr[Model.BIAS_VEC]

        """
        return self._run_model(self.layer_count - 1, input)
        """
        return input


    # recursive implementation (maybe its better without Python objects getting in the way?)
    def _run_model(self, lyr_idx, input):
        if lyr_idx < 0: return input

        return self._run_model(
            lyr_idx - 1,
            self.layers[lyr_idx][Model.WGHT_MATRIX] @ input + self.layers[lyr_idx][Model.BIAS_VEC],
        )


    def save_model(self):  # need to define a model file structure
        pass
