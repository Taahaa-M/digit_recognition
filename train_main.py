from model import Model
from digit import Digits
from trainer import Trainer

DIGITS_FILE_NAME = "archive/train-images.idx3-ubyte"
DIGIT_LABELS_FILE_NAME = "archive/train-labels.idx1-ubyte"

DIGITS_TEST_FILE_NAME = "archive/t10k-images.idx3-ubyte"
DIGITS_TEST_LABELS_FILE_NAME = "archive/t10k-labels.idx1-ubyte"

def main():
    digits = Digits(
        DIGITS_FILE_NAME,
        DIGIT_LABELS_FILE_NAME
    )

    test_digits = Digits(
        DIGITS_TEST_FILE_NAME,
        DIGITS_TEST_LABELS_FILE_NAME
    )

    digit_vectors = digits.get_digits_list()
    digit_label_vectors = digits.get_digit_labels_list()

    test_digit_vectors = test_digits.get_digits_list()
    test_digit_label_vectors = test_digits.get_digit_labels_list()

    model = Model(
        input_size=digits.get_image_size(),
        output_size=10,
        neuron_count_list=[digits.get_image_size(), 128, 64, 10]
    )

    epoch_count = 1000
    trainer = Trainer(model, digit_vectors, digit_label_vectors)
    trainer.train_model(epoch_count, learning_rate=100.0)

    print("\nWith test data:")
    trainer.test(test_digit_vectors, test_digit_label_vectors)
    print("\nWith training data:")
    trainer.test(digit_vectors, digit_label_vectors)

    if input("Do you want to save this model?").lower() == 'y':
        model.save_model("mnist_sigmoid_model.npz")


if __name__ == "__main__":
    main()
