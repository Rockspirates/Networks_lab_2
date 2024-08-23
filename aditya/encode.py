import qrcode
import numpy as np
import wave
from scipy.signal import find_peaks
from pyzbar.pyzbar import decode
import cv2

def bitstring_to_qr_matrix(bitstring):
    # Convert bitstring to a string of '0' and '1' characters
    bitstring_data = ''.join(['1' if bit=='1' else '0' for bit in bitstring])
    
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=1,
        border=0,
    )
    qr.add_data(bitstring_data)
    qr.make(fit=True)

    # Get the QR code matrix (2D array)
    qr_matrix = qr.get_matrix()
    
    return qr_matrix 

def qr_matrix_flatten(matrix):
    s= []
    for row in matrix:
        for x in row:
            y= 1 if x else 0
            s.append(y)
    return s

# encode flatten to audio
def bitstring_to_fm_audio(bitstring, bit_duration=0.1, f0=440, f1=880, samplerate=44100):
    """
    Convert a bitstring to a frequency-modulated audio signal.
    
    :param bitstring: A string of '0's and '1's.
    :param bit_duration: Duration of each bit in seconds.
    :param f0: Frequency for '0' in Hz.
    :param f1: Frequency for '1' in Hz.
    :param samplerate: Sampling rate in Hz.
    :return: A numpy array representing the audio signal.
    """
    # Number of samples per bit
    num_samples = int(samplerate * bit_duration)
    
    # Initialize an empty list to hold the audio samples
    audio = []
    
    # Generate the audio signal for each bit
    for bit in bitstring:
        if bit == 0:
            frequency = f0
        elif bit == 1:
            frequency = f1
        else:
            raise ValueError("Bitstring can only contain '0' and '1'.")

        t = np.linspace(0, bit_duration, num_samples, False)
        wave = np.sin(2 * np.pi * frequency * t) * 32767  # Generate sine wave for the bit
        audio.append(wave)

    # Concatenate all the waves into a single array
    audio = np.concatenate(audio).astype(np.int16)
    
    return audio

# # Example bitstring
# bitstring = "101010011010"

# # Convert the bitstring to an audio signal
# audio = bitstring_to_fm_audio(bitstring)

# # Play the audio
# play_obj = sa.play_buffer(audio, 1, 2, 44100)
# play_obj.wait_done()


def save_audio_to_wav(audio, filename, samplerate=44100):
    """
    Save the audio signal as a WAV file.
    
    :param audio: A numpy array representing the audio signal.
    :param filename: The output filename for the WAV file.
    :param samplerate: Sampling rate in Hz.
    """
    with wave.open(filename, 'w') as wav_file:
        # Set parameters: nchannels, sampwidth, framerate, nframes, comptype, compname
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit audio
        wav_file.setframerate(samplerate)
        wav_file.writeframes(audio.tobytes())

# # Example usage
# wave_file = "recorded_audio.wav"  # Replace with your recorded WAV file path
# decoded_bitstring = audio_to_bitstring(wave_file)

# decode audio to flatten
def qr_matrix_to_bitstring(qr_matrix):
    """
    Decode a QR matrix (2D list or numpy array) to extract the encoded information.
    
    :param qr_matrix: A 2D list or numpy array representing the QR code.
    :return: The decoded data from the QR code.
    """
    # Convert the QR matrix (2D list) to a numpy array if it's not already
    qr_array = np.array(qr_matrix, dtype=np.uint8) * 255  # Convert 0/1 to 0/255 (black/white)
    
    # Convert to a format that pyzbar can read
    qr_image = cv2.cvtColor(qr_array, cv2.COLOR_GRAY2BGR)
    
    # Use pyzbar to decode the QR code
    decoded_objects = decode(qr_image)
    
    for obj in decoded_objects:
        return obj.data.decode("utf-8")  # Assuming it's UTF-8 encoded text

    return None  # Return None if no QR code is found

import cv2
from pyzbar.pyzbar import decode

def decode_qr_image(qr_image):
    """
    Decode the binary QR image to extract the data.
    
    :param qr_image: The binary image of the QR code.
    :return: The decoded data from the QR code.
    """
    # Convert the image to a 3-channel BGR format as required by pyzbar
    
    # Decode the QR code using pyzbar
    decoded_objects = decode(qr_image)
    
    # Extract and return the decoded data
    for obj in decoded_objects:
        return obj.data.decode('utf-8')  # Assuming UTF-8 encoded text

    return None  # If no QR code is found

bitstring = "1110010001110101"
audio_name = "aditya.wav"

save_audio_to_wav(bitstring_to_fm_audio(qr_matrix_flatten(bitstring_to_qr_matrix(bitstring))),audio_name)






















































