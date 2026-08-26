import sys
import numpy as np
import struct


class Digits():
    def __init__(self, digits_file, digit_labels_file):
        self._read_digits(digits_file)
        self._read_digit_labels(digit_labels_file)

    def _read_digits(self, digits_file):
        with open(digits_file, "rb") as f:
            header = f.read(16)

            # 4 big-endian uint32
            magic, count, rows, cols = struct.unpack(">IIII", header)

        try:
            assert(magic==2051)
        except:
            print(f"{digits_file} is an invalid digits file. Use the MNIST dataset", file=sys.stderr)
            quit()

        self.digits_list = [np.empty(shape=(rows * cols,), dtype=np.float64) for _ in range(count)]


    def _read_digit_labels(self, digit_labels_file):
        with open(digit_labels_file, "rb") as f:
            header = f.read(8)

            # 2 big-endian uint32
            magic, label_count = struct.unpack(">II", header)

        try:
            assert(magic==2051)
        except:
            print(f"{digit_labels_file} is an invalid labels file. Use the MNIST dataset", file=sys.stderr)
            quit()

        self.digit_labels_list = [
            np.empty(
                shape=(10,),
                dtype=np.float64
            ) for _ in range(label_count)
        ]


    def get_digits_list(self):
        pass


    def get_digit_labels_list(self):
        pass
