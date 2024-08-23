import wave
import numpy as np
import matplotlib.pyplot as plt

# Load the .wav file
file_name = 'sine_wave.wav'
with wave.open(file_name, 'rb') as wf:
    sample_rate = wf.getframerate()
    n_frames = wf.getnframes()
    n_channels = wf.getnchannels()
    samp_width = wf.getsampwidth()
    audio_data = wf.readframes(n_frames)

# Convert audio data to numpy array
audio_data = np.frombuffer(audio_data, dtype=np.int16)

# If stereo, select one channel
if n_channels > 1:
    audio_data = audio_data[::n_channels]

print(n_frames, sample_rate)

# Generate time axis in milliseconds
t = np.linspace(0, 1, 100)
# Convert to milliseconds
t1 = np.linspace(1, 2, 100)
time_axis = np.concatenate((t,t1))
# Plot the waveform
plt.figure(figsize=(10, 4))
plt.plot(time_axis, audio_data, label="Amplitude")
plt.xlabel('Time [ms]')
plt.ylabel('Amplitude')
plt.title(f'Waveform of {file_name}')
plt.legend()
plt.grid(True)
plt.show()
