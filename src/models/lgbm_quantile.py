"""LightGBM quantile regression: one model per quantile."""


class LGBMQuantileModel:
    def __init__(self, quantiles=(0.1, 0.5, 0.9)):
        self.quantiles = quantiles

    def fit(self, X, y):
        raise NotImplementedError

    def predict(self, X):
        raise NotImplementedError
