import numpy as np
import pyaudio
import wave

def save_sound_to_wav(filename, samples, sample_rate=44100):
    """
    Saves the given samples to a WAV file.

    :param filename: The name of the file to save the audio.
    :param samples: Numpy array of samples to save.
    :param sample_rate: Sampling rate in samples per second.
    """
    # Convert to 16-bit data
    samples = (samples * 32767).astype(np.int16)

    # Open a wave file
    with wave.open(filename, 'w') as wav_file:
        # Set parameters: nchannels, sampwidth, framerate, nframes, comptype, compname
        wav_file.setnchannels(1)  # mono
        wav_file.setsampwidth(2)  # 16 bits = 2 bytes
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(samples.tobytes())


def generate_cosine_wave(frequency=100, duration=0.5, volume=1 , sample_rate=44100, phase=0):
    """
    Generates a cosine wave with a specified phase shift.

    :param frequency: Frequency of the cosine wave in Hertz.
    :param duration: Duration of the sound in seconds.
    :param volume: Volume of the sound (0.0 to 1.0).
    :param sample_rate: Sampling rate in samples per second.
    :param phase: Phase shift in radians (0 to 2π).
    :return: Numpy array of samples.
    """
    # Generate time points
    t = np.linspace(0, duration, int(sample_rate * duration), False)

    # Generate cosine wave with phase shift
    samples = volume * np.cos(2 * np.pi * frequency * t + phase)

    return samples

def play_sound(p, samples, sample_rate=44100):
    """
    Plays the given samples using PyAudio.

    :param p: PyAudio object.
    :param samples: Numpy array of samples to play.
    :param sample_rate: Sampling rate in samples per second.
    """
    # Convert to 16-bit data
    samples = (samples * 32767).astype(np.int16).tobytes()

    # Open audio stream
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=sample_rate,
                    output=True)

    # Play sound
    stream.write(samples)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()

p = pyaudio.PyAudio()

# bitstring = input("Enter a bitstring: ")

bitstring = "10101010"

n = len(bitstring)
combined_samples = np.array([])  # Initialize an empty array for combining samples

# Generate and combine the samples for each bit pair
for i in range(0, n, 2):
    if bitstring[i:i+2] == "00":
        print("Generating 00")
        samples = generate_cosine_wave(phase=0)
    elif bitstring[i:i+2] == "01":
        print("Generating 01")
        samples = generate_cosine_wave(phase=np.pi/2)
    elif bitstring[i:i+2] == "10":
        print("Generating 10")
        samples = generate_cosine_wave(phase=np.pi)
    elif bitstring[i:i+2] == "11":
        print("Generating 11")
        samples = generate_cosine_wave(phase=3*np.pi/2)
    
    # Concatenate the current samples to the combined array
    combined_samples = np.concatenate((combined_samples, samples))

play_sound(p, combined_samples)


file_name = "output.wav"
# Play the combined sound at once
save_sound_to_wav(file_name, combined_samples)

p.terminate()
