import pandas
import numpy as np
import os
import matplotlib.pyplot as plt

def load(filename, delimiter, skiprows=0):
    """
Loads a measurement file in a robust manner
    """
    # Load s-params file
    path = os.path.join(os.path.dirname(__file__), filename)
    data = pandas.read_csv(path,skiprows=skiprows, delimiter=delimiter).as_matrix()

    return data

def analyse(name, arr):
    print("Array : ", name)
    print("shape : ", arr.shape)

def convert(sfreqs, s21_mag, s21_phase, t_wvf, v_wvf,sampling=1.0):
    # Compute fft of voltage waveform
    fft = np.fft.rfft(v_wvf)
    fft_freq = np.fft.rfftfreq(v_wvf.shape[-1],d=sampling)

    # Interpolate sensor response to match fft frequencies
    s21_mag_i = np.interp(fft_freq, sfreqs, s21_mag)
    s21_phase_i = np.interp(fft_freq, sfreqs, s21_phase)

    # Convert sensor magnitude/phase to complex domain, converting dB appropriately
    sensor_complex = np.power(10,s21_mag_i/20) * ( np.cos(s21_phase_i) + 1j * np.sin(s21_phase_i) )

    # Apply sensor response
    fft_compensated = fft / sensor_complex

    # Compute inverse fft
    voltage = np.fft.irfft(fft_compensated)
    # Recompute matching x-scale
    time = np.linspace(t_wvf[0],t_wvf[-1], num=voltage.shape[0])

    # Remove DC offset (poorly)
    voltage -= voltage[0]

    return time, voltage

def xslice(x, y, xmin, xmax):
    arr = np.vstack((x, y)).T
    arr = np.array([e for e in arr if e[0] >= xmin and e[0] <= xmax])
    return arr.T[0], arr.T[1]

def check_constant_sample_rate(t):
    intervals = t[1:] - t[:-1]
    for interval in intervals:
        if not np.isclose(interval, intervals[0]):
            return False
    return True

def check_strictly_monotonic(t):
    assert len(t) == len(y)
    toremove = [i for i in range(len(t) - 1) if np.isclose(t[i],t[i+1])]
    return len(toremove) == 0

def make_strictly_monotonic(t, y):
    assert len(t) == len(y)
    tokeep = [i for i in range(len(t) - 1) if not np.isclose(t[i],t[i+1])]
    t = np.take(t, tokeep)
    y = np.take(y, tokeep)
    return t, y
    
if __name__ == '__main__':
    print(xslice(np.arange(10),np.linspace(0,1,10), 3, 5))
