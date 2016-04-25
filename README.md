# Near-field current measurement post-processing
This python script compares frequency-domain and time-domain method to performs
post-processing of a passive near field current sensor.

Near-field current sensor produces a voltage waveform when exposed to a current.
This voltage waveform is somehow the derivative of the original current waveform.

The goal of this script is to reconstitute the original current waveform from the
voltage waveform.

# Run
```
python run.py
```

# Acknowledgements
Thanks to Fabien Escudie for the algorithm and feedback
