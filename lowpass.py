import wave
import numpy as np

def low_pass_filter(input_file, output_file, cutoff_freq):
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

    # Apply the low-pass filter by zeroing out frequencies above the cutoff
    fft_result[np.abs(frequencies) > cutoff_freq] = 0

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
input_file = 'output.wav'    # Input .wav file
output_file = 'output.wav'  # Output .wav file
cutoff_freq = 650  # Cutoff frequency in Hz

# Apply low-pass filter
low_pass_filter(input_file, output_file, cutoff_freq)
