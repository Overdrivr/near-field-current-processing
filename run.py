from postprocess import load, convert, analyse
import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate
import json
import sys
import fileinput

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print()
        sys.exit("No config filename provided during script invocation")

    # Load json config
    f = open(sys.argv[1], 'r')
    cfg = json.load(f)

    # Load S-parameters measurement
    d = load(cfg['characterization']['s_params']['filename'],
             cfg['characterization']['s_params']['delimiter'],
             skiprows=cfg['characterization']['s_params']['skiprows'])

    freqs = d[:,cfg['characterization']['s_params']['columns']['freq']]
    mag   = d[:,cfg['characterization']['s_params']['columns']['S21_mag']]
    phase = d[:,cfg['characterization']['s_params']['columns']['S21_phase']]

    #TODO: Replace by a json specific config entry
    # 1st Method : frequency domain
    # Add a frequency point at 0
    freqs = np.insert(freqs, 0, freqs[0]/1e5)
    mag = np.insert(mag, 0, mag[0] - 100)
    phase = np.insert(phase, 0, phase[0])
    # Convert phase to 0
    phase = np.radians(phase)

    if cfg['characterization']['s_params']['plot']:
        plt.subplot(2, 1, 1)
        plt.semilogx(freqs, mag)
        plt.title("S21 characterization of current sensor")
        plt.ylabel("S21 magnitude (dB)")
        plt.subplot(2, 1, 2)
        plt.semilogx(freqs, phase)
        plt.ylabel("S21 phase (degrees)")
        plt.xlabel("Frequency (Hz)")
        plt.show()

    # Load transient voltage waveform to be post-processed
    d = load(cfg['output']['waveform']['filename'],
             cfg['output']['waveform']['delimiter'],
             skiprows=cfg['output']['waveform']['skiprows'])

    time    = d[:,cfg['output']['waveform']['columns']['time']]
    voltage = d[:,cfg['output']['waveform']['columns']['voltage']]

    # Perform post-processing of the transient voltage waveform
    processed_time, processed_voltage = convert(freqs, mag, phase, time, voltage,
            sampling=cfg['output']['waveform']['sampling_period'])

    # TODO: JSON
    processed_voltage /= 20

    # 2nd Method : Integration
    # Perform integration-based reconstitution method of the current waveform
    integral = integrate.cumtrapz(voltage, time, initial=0)
    # Apply gain
    integral *= 8e8

    if 'reference' in cfg:
        d = load(cfg['reference']['waveform']['filename'],
                 cfg['reference']['waveform']['delimiter'],
                 skiprows=cfg['reference']['waveform']['skiprows'])

        ref_time    = d[:,cfg['reference']['waveform']['columns']['time']]
        ref_current = d[:,cfg['reference']['waveform']['columns']['current']]
    else:
        ref_time = [0]
        ref_current = [0]

    # Final plot
    original, = plt.plot(ref_time, ref_current, label="original curve")
    trap, = plt.plot(time, integral, label="integral method")
    final, = plt.plot(processed_time, processed_voltage, label="frequency method")
    plt.legend(handles=[original,trap,final])
    plt.show()

    np.savetxt("output.csv", [processed_time, processed_voltage], delimiter='\t', header='time (s)\tV(t)')
