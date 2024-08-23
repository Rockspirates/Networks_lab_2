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

# Perform Fourier Transform
fft_result = np.fft.fft(audio_data)
frequencies = np.fft.fftfreq(n_frames, d=1/sample_rate)

# Get the magnitude of the Fourier Transform
magnitude = np.abs(fft_result)

# Plot the frequencies and their magnitudes
plt.figure(figsize=(10, 6))
plt.plot(frequencies[:n_frames // 2], magnitude[:n_frames // 2])  # Plot only positive frequencies
plt.xlabel('Frequency [Hz]')
plt.ylabel('Magnitude')
plt.title(f'Frequency Spectrum of {file_name}')
plt.grid(True)
plt.show()
