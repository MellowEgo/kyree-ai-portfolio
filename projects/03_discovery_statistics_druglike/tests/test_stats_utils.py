import numpy as np
import scipy.stats as st

def anova_oneway(*groups):
    return st.f_oneway(*groups)