"""Rolling-origin backtest loop."""


def run_backtest(model, df, start: str, end: str, horizon: int = 24):
    """Refit and forecast over rolling origins; return per-origin metrics."""
    raise NotImplementedError
