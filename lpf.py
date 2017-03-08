from postprocess import load, check_constant_sample_rate
import numpy as np
from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

if __name__ == '__main__':
    d = load('./datafiles/simulation_TLP_minus480V.csv', delimiter=',', skiprows=15)
    t = d[:,0]
    v1 = d[:,1]
    v2 = d[:,2]

    if not check_constant_sample_rate(t):
        # Remove points where timestep is 0
        tokeep = [i for i in range(len(t) - 1) if not np.isclose(t[i],t[i+1],atol=1e-15)]

        print("Removed ", len(t) - len(tokeep), ' on ', len(tokeep))

        ti = np.take(t, tokeep)
        v1i = np.take(v1, tokeep)
        v2i = np.take(v2, tokeep)

        # Compute deltas
        deltas = ti[1:] - ti[:-1]
        # Find lowest delta
        lowest = np.amin(deltas)
        print('Lowest delta: ', lowest)
        # Arange samples
        tsamples = np.arange(ti[0], ti[-1], lowest)
        # Interpolate variable step data along fixed step points
        v1i = np.interp(tsamples, ti, v1i)
        v2i = np.interp(tsamples, ti, v2i)

    samples = [ti[i] - ti[i-1] for i in range(len(ti) - 1) if ti[i] - ti[i-1] != 5e-10]

    # Filter requirements.
    order = 2
    fs = 1 / (ti[1] - ti[0])       # sample rate, Hz
    cutoff = 1e7  # desired cutoff frequency of the filter, Hz

    y = butter_lowpass_filter(v1i, cutoff, fs, order=order)

    plt.plot(t, v1, 'b-', label='raw')
    plt.plot(tsamples, v1i, 'r-', label='interp')
    plt.plot(tsamples, y, 'g-', linewidth=2, label='filtered')
    plt.xlabel('Time [sec]')
    plt.grid()
    plt.legend()
    plt.show()
