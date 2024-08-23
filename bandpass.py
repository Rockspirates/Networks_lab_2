import wave
import numpy as np

def bandpass_filter(input_file, output_file, low_cutoff_freq, high_cutoff_freq):
    # Load the .wav file
    with wave.open(input_file, 'rb') as wf:
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

    # Apply the bandpass filter by zeroing out frequencies outside the desired range
    fft_result[(np.abs(frequencies) < low_cutoff_freq) | (np.abs(frequencies) > high_cutoff_freq)] = 0

    # Perform Inverse Fourier Transform to convert back to time domain
    filtered_audio_data = np.fft.ifft(fft_result).real

    # Convert to 16-bit PCM
    filtered_audio_data = np.int16(filtered_audio_data)

    # Save the filtered audio data to a new .wav file
    with wave.open(output_file, 'wb') as wf:
        wf.setnchannels(1)  # Mono channel
        wf.setsampwidth(samp_width)
        wf.setframerate(sample_rate)
        wf.writeframes(filtered_audio_data.tobytes())

    print(f"Filtered audio saved to {output_file}")

# Parameters
input_file = 'sine_wave.wav'    # Input .wav file
output_file = 'bandpass_filtered.wav'  # Output .wav file
low_cutoff_freq = 1000  # Lower cutoff frequency in Hz
high_cutoff_freq = 4000  # Upper cutoff frequency in Hz

# Apply bandpass filter
bandpass_filter(input_file, output_file, low_cutoff_freq, high_cutoff_freq)
