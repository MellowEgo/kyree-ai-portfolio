import numpy as np

def wmape(y_true, y_pred, eps: float = 1e-9):
    y_true = np.asarray(y_true, dtype=float); y_pred = np.asarray(y_pred, dtype=float)
    denom = np.abs(y_true).sum()
    return float(np.abs(y_true - y_pred).sum() / max(denom, eps))

def mase(y_true, y_pred, seasonality=1, eps: float = 1e-9):
    y_true = np.asarray(y_true, dtype=float); y_pred = np.asarray(y_pred, dtype=float)
    mae = np.mean(np.abs(y_true - y_pred))
    if len(y_true) <= seasonality:
        d = np.mean(np.abs(np.diff(y_true)))
    else:
        d = np.mean(np.abs(y_true[seasonality:] - y_true[:-seasonality]))
    return float(mae / max(d, eps))
