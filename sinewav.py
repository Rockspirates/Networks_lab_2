import numpy as np
import wave

# Parameters
sample_rate = 44100  # Sampling rate in Hz
duration = 1.0  # Duration in seconds
frequency = 5000.0  # Frequency of the sine wave in Hz

# Generate the sine wave
t = np.linspace(0, duration, 100)
sine_wave = 0.5 * np.sin(2 * np.pi * t)
t1 = np.linspace(1, 2, 100)
sine_wave_1 = 1 * np.sin(2 * np.pi * t1)

sine_wave = np.concatenate((sine_wave, sine_wave_1))
print(sine_wave)

# Convert to 16-bit data
audio_data = (sine_wave * 32767).astype(np.int16)

# Save the audio to a .wav file
with wave.open("sine_wave.wav", "wb") as wf:
    wf.setnchannels(1)  # Mono channel
    wf.setsampwidth(2)  # 2 bytes per sample (16-bit audio)
    wf.setframerate(sample_rate)
    wf.writeframes(audio_data.tobytes())

print("sine_wave.wav generated successfully!")
