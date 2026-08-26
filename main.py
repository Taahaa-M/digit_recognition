from model import Model
from digit import Digits
from trainer import Trainer

DIGITS_FILE_NAME = "archive/train-images.idx3-ubyte"
DIGIT_LABELS_FILE_NAME = "archive/train-labels.idx1-ubyte"

def main():
    digits = Digits(
        DIGITS_FILE_NAME,
        DIGIT_LABELS_FILE_NAME
    )

    labels = digits.get_digit_labels_list()
    for i in range(10):
        print(labels[i])


if __name__ == "__main__":
    main()
