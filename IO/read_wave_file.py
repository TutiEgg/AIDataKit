from scipy.io import wavfile
import numpy as np
import math
import matplotlib.pyplot as plt

samplerate, data = wavfile.read('./output.wav')
print("sample_rate:", samplerate)

# get time in seconds
num_of_samples = data.shape[0]
time_in_sec = math.ceil(num_of_samples/samplerate)
print("overall time:", time_in_sec)
time_step = 1/samplerate

# create time plot
time_values = np.linspace(0, time_in_sec, num_of_samples)

plt.plot(time_values[0:10000], data[0:10000])
plt.show()


