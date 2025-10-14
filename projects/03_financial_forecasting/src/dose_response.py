import numpy as np
from scipy.optimize import curve_fit

def four_pl(x, a, b, c, d):
    return d + (a - d) / (1 + (x / c)**b)

def fit_4pl(x, y):
    popt, pcov = curve_fit(four_pl, x, y, maxfev=10000)
    return popt, pcov