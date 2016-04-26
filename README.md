# Near-field current measurement post-processing
This python script compares frequency-domain and time-domain method to performs
post-processing of a passive near field current sensor.

Near-field current sensor produces a voltage waveform when exposed to a current.
This voltage waveform is somehow the derivative of the original current waveform.

The goal of this script is to reconstitute the original current waveform from the
voltage waveform.

# Run
```
python run.py config_remi.py
```

# Requirements

* `matplotlib`, `numpy`, `scipy`

# Post-process your own data

1. Copy `config_remi.json` configuration file and rename it to your own name
2. Modify all fields to match your own data files (filepath, column delimiters,etc.)
3. Run the script and don't forget to pass your custom config file as last argument

# Acknowledgements
Thanks to Fabien Escudie for the algorithm and feedback
