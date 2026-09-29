"""PyTorch multi-quantile neural network model."""


class TorchQuantileModel:
    def __init__(self, quantiles=(0.1, 0.5, 0.9)):
        self.quantiles = quantiles

    def fit(self, X, y):
        raise NotImplementedError

    def predict(self, X):
        raise NotImplementedError
