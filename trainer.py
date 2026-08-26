from model import Model
from digit import Digits

class Trainer():
    def __init__(
        self,
        model,
        digits,
        digits_batch_size=None
    ):
        self._model = model
        self._digits = digits
