from postprocess import check_constant_sample_rate, make_strictly_monotonic
import numpy as np

def test_detect_constant_rate():
    constant = np.linspace(0,1,10)
    assert check_constant_sample_rate(constant)

def test_detect_not_constant_rate():
    nonconstant = np.linspace(0,1,10)
    nonconstant[3] = 0.3
    assert not check_constant_sample_rate(nonconstant)

def make_strictly_monotonic():
    t = np.linspace()
