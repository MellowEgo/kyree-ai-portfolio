from projects.03_financial_forecasting.src.evaluation.metrics import wmape, mase
import numpy as np

def test_wmape_range():
    y, yhat = np.array([10,10,10]), np.array([9,11,10])
    assert 0 <= wmape(y,yhat) <= 1

def test_mase_nonneg():
    y, yhat = np.array([1,2,3,4,5]), np.array([1,2,3,4,5])
    assert mase(y,yhat) >= 0
