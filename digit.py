import sys
import numpy as np
import struct


class Digits():
    DIGITS_MAGIC_NO = 2051
    LABELS_MAGIC_NO = 2049
    def __init__(self, digits_file, digit_labels_file):
        self._read_digits(digits_file)
        self._read_digit_labels(digit_labels_file)

        try:
            assert(self._label_count == self._count)
        except Exception as e:
            print(e, file=sys.stderr)
            print(f"lbl_count={self._label_count}\n"
                + f"img_count={self._count}\n",
                file=sys.stderr
            )
            print(
                f"Using this Digits object ({self}) is not advised.\n" +
                "Behaviour will be undefined.\n",
                file=sys.stderr
            )


    def _read_digits(self, digits_file):
        with open(digits_file, "rb") as f:
            # 4 big-endian uint32
            header = f.read(int(4*32/8))
            magic, count, rows, cols = struct.unpack(">IIII", header)

            try:
                assert(magic == Digits.DIGITS_MAGIC_NO)
            except:
                print(f"{digits_file} is an invalid digits file. Use the MNIST dataset", file=sys.stderr)
                return

            self._count = count
            self._rows = rows
            self._cols = cols

            self._digits_list = [None] * count  # everything is a pointer type, right?
            for i in range(count):
                self._digits_list[i] = np.fromfile(
                    f,
                    dtype=np.uint8,
                    count=(rows * cols)
                ).astype(np.float64) / float(2**8)


    def _read_digit_labels(self, digit_labels_file):
        with open(digit_labels_file, "rb") as f:
            header = f.read(8)

            # 2 big-endian uint32
            magic, label_count = struct.unpack(">II", header)

            try:
                assert(magic == Digits.LABELS_MAGIC_NO)
            except:
                print(f"{digit_labels_file} is an invalid labels file. Use the MNIST dataset", file=sys.stderr)
                return

            self._label_count = label_count

            self._digit_labels_list = list(
                np.zeros(shape=(10,), dtype=np.float64)
                for _ in range(label_count)
            )
            for i in range(label_count):
                header = f.read(1)
                self._digit_labels_list[i][struct.unpack("B", header)] = 1.0
                # label '0' will be the first in the array at idx 0


    def get_digits_list(self):
        return self._digits_list


    def get_digit_labels_list(self):
        return self._digit_labels_list


    def get_image_size(self):
        return self._rows * self._cols
