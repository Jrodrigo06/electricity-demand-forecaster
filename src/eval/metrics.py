"""Probabilistic forecast metrics."""


def pinball_loss(y_true, y_pred, quantile: float) -> float:
    """Pinball (quantile) loss for a single quantile."""
    raise NotImplementedError


def coverage(y_true, lower, upper) -> float:
    """Fraction of observations falling inside [lower, upper]."""
    raise NotImplementedError
