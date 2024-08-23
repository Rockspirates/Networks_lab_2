import wave
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert

def plot_extra_phase(input_file):
    # Load the .wav file
    with wave.open(input_file, 'rb') as wf:
        sample_rate = wf.getframerate()
        n_frames = wf.getnframes()
        n_channels = wf.getnchannels()
        audio_data = wf.readframes(n_frames)

    # Convert audio data to numpy array
    audio_data = np.frombuffer(audio_data, dtype=np.int16)

    # If stereo, select one channel
    if n_channels > 1:
        audio_data = audio_data[::n_channels]
    # Compute the analytic signal using the Hilbert transform
    analytic_signal = hilbert(audio_data)
    # Calculate the instantaneous phase
    instantaneous_phase = np.angle(analytic_signal)

    # Create a time array
    time = np.linspace(0, n_frames / sample_rate, n_frames, endpoint=False)

    # Calculate the linear phase component
    linear_phase = 2 * np.pi * time * np.max(np.abs(audio_data))  # Scale the frequency appropriately

    # Calculate the extra phase by subtracting the linear phase from the instantaneous phase
    extra_phase = instantaneous_phase - linear_phase

    # Plot extra phase over time
    plt.figure(figsize=(10, 6))
    plt.plot(time, extra_phase, label='Extra Phase')
    plt.title('Extra Phase Over Time')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Extra Phase (radians)')
    plt.xlim(0, time[-1])  # Limit x-axis to the duration of the signal
    plt.grid(True)
    plt.legend()
    plt.show()

# Parameters
input_file = 'sine_wave.wav'  # Replace with your audio file name

# Plot the extra phase over time
plot_extra_phase(input_file)
