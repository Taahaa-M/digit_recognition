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

    digit_vectors = digits.get_digits_list()
    digit_label_vectors = digits.get_digit_labels_list()

    model = Model(
        input_size=digits.get_image_size(),
        output_size=10,
        neuron_count_list=[digits.get_image_size(), 128, 64, 10]
    )

    trainer = Trainer(model, digit_vectors, digit_label_vectors)
    trainer.train_model()


if __name__ == "__main__":
    main()
