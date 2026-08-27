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
        self.layer_count = len(neuron_count_list) - 1
        self.pre_norm_lyr_output = [None] * self.layer_count
        self.norm_lyr_output = [None] * self.layer_count

        for i in range(self.layer_count):
            lyr_input_size = neuron_count_list[i]
            lyr_output_size = neuron_count_list[i+1]

            self.layers.append([
                np.random.default_rng().normal(  # weight matrix
                    0.0,
                    np.sqrt(2.0 / lyr_input_size),
                    size=(lyr_output_size, lyr_input_size),
                ),
                np.zeros(                        # bias vector
                    shape=(lyr_output_size, 1),
                    dtype=np.float64,
                )
            ])


    def run_model(self, input, norm_func):
        for i in range(self.layer_count):
            self.pre_norm_lyr_output[i] = self.layers[i][Model.WGHT_MATRIX] @ input \
                + self.layers[i][Model.BIAS_VEC]
            input = self.norm_lyr_output[i] = norm_func(self.pre_norm_lyr_output[i])

        return input


    def save_model(self):  # need to define a model file structure
        pass
