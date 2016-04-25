from postprocess import load, convert, analyse
import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate

sparams_file = "sensor_sparams.csv"
voltage_file = "transient_waveform_10V.csv"
voltage_sampling_period = 8e-12 # Scope sample frequency
reference_file = "reference_i_measurement.csv"

# Load S-parameters measurement
d = load(sparams_file,' |\t', skiprows=3)
freqs = d[:,0]
mag = d[:,1]
phase = d[:,2]

# 1st Method : frequency domain
# Add a frequency point at 0
freqs = np.insert(freqs, 0, freqs[0]/1e5)
mag = np.insert(mag, 0, mag[0] - 100)
phase = np.insert(phase, 0, phase[0])
# Convert phase to 0
phase = np.radians(phase)

# Load transient voltage waveform to be post-processed
d = load(voltage_file, ',', skiprows=5)
time = d[:,3]
voltage = d[:,4]

# Perform post-processing of the transient voltage waveform
processed_time, processed_voltage = convert(freqs, mag, phase, time, voltage, sampling=voltage_sampling_period)
processed_voltage /= 20

# 2nd Method : Integration
# Perform integration-based reconstitution method of the current waveform
integral = integrate.cumtrapz(voltage, time, initial=0)
# Apply gain
integral *= 8e8

# 3rd Method : original TLP measurmement of injected current
# Load reference current measurement (TLP measurement)
d = load(reference_file, '\t', skiprows=1)
ref_time = d[:,0]
ref_current = d[:,2]


# Final plot
original, = plt.plot(ref_time, ref_current, label="original curve")
trap, = plt.plot(time, integral, label="integral method")
final, = plt.plot(processed_time, processed_voltage, label="frequency method")
plt.legend(handles=[original,trap,final])
plt.show()
