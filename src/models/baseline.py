"""Baseline forecasters (e.g. seasonal naive with empirical quantiles)."""


class BaselineModel:
    def fit(self, X, y):
        raise NotImplementedError

    def predict(self, X):
        raise NotImplementedError
