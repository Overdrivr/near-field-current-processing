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

def prepare():
    pass

def convert(sfreqs, s21_mag, s21_phase, t_wvf, v_wvf,sampling=1.0):
    # Compute fft of voltage waveform
    fft = np.fft.rfft(v_wvf)
    fft_freq = np.fft.rfftfreq(v_wvf.shape[-1],d=sampling)
    #fft_freq = np.fft.fftshift(fft_freq)

    # Interpolate sensor response to match fft frequencies
    s21_mag_i = np.interp(fft_freq, sfreqs, s21_mag)
    s21_phase_i = np.interp(fft_freq, sfreqs, s21_phase)

    # Convert sensor magnitude/phase to complex domain
    #TODO: Convert from dB to amplitude !
    #sensor_complex = np.power(10,s21_mag_i/20) * np.exp(1j * s21_phase_i)
    sensor_complex = np.power(10,s21_mag_i/20) * ( np.cos(s21_phase_i) + 1j * np.sin(s21_phase_i) )
    #complex((10^(gain_sonde(cte)/20)*cos((pi*phase_sonde(cte))/180)),(10^(gain_sonde(cte)/20)*sin((pi*phase_sonde(cte))/180)));
    print(sensor_complex)

    # Apply sensor response
    fft_compensated = fft / sensor_complex

    plt.plot(fft_freq,fft.real,fft_freq,fft.imag)
    plt.show()

    # Compute inverse fft
    voltage = np.fft.irfft(fft_compensated)

    time = np.linspace(t_wvf[0],t_wvf[-1], num=voltage.shape[0])
    #print(v.shape)
    #up, = plt.plot(np.linspace(t_wvf[0], t_wvf[-1],v.shape[0]), v, label="post-processed")
    #down, = plt.plot(t_wvf, v_wvf, label="original")
    #plt.legend(handles=[up,down])
    #plt.show()

    voltage -= voltage[0]
    voltage /= 5

    return time, voltage
