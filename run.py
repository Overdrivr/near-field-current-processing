from postprocess import load, convert, analyse
import numpy as np
import matplotlib.pyplot as plt

sparams_file = "sensor.csv"
voltage_file = "passthrough_sensor_10V.csv"

d = load(sparams_file,' |\t', skiprows=3)
freqs = d[:,0]
mag = d[:,1]
phase = d[:,2]

## SENSOR PROCESSING
# Add a frequency point at 0
freqs = np.insert(freqs, 0, freqs[0]/1e5)
mag = np.insert(mag, 0, mag[0] - 100)
phase = np.insert(phase, 0, phase[0])

phase = np.radians(phase)

d = load(voltage_file, ',', skiprows=5)
time = d[:,3]
voltage = d[:,4]

#plt.semilogx(freqs, mag, freqs, phase)
#plt.show()

# Test data
#time = np.arange(0,3,0.0001)
#voltage = np.sin(2 * np.pi * 10 * time + np.pi)

# Test data 2
#N=600
#T = 1.0 / 800.0
#time = np.linspace(0.0, N*T, N)
#voltage = np.sin(50.0 * 2.0*np.pi*time) + 0.5*np.sin(80.0 * 2.0*np.pi*time)

analyse("S params frequency points", freqs)
analyse("Time-domain points", time)


#plt.plot(time, voltage, label="transient waveform")
#plt.show()

# Process values
#convert(sparams[:,0], sparams[:,3], v_wvf[:,3], v_wvf[:,4],sampling=8e-12)
processed_time, processed_voltage = convert(freqs, mag, phase, time, voltage, sampling=8e-12)

# Final plot
original, = plt.plot(time, voltage, label="original curve")
print(type(processed_time[0]))
print(type(processed_voltage[0]))
final, = plt.plot(processed_time, processed_voltage, label="final curve")
plt.legend(handles=[original,final])
plt.show()

analyse("Post processed voltage waveform", processed_voltage)
