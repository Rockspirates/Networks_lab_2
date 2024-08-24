from PIL import Image
import numpy as np
import wave
import cv2

audio_name = "aditya.wav"
image_name = 'decode.png'

def convert_matrix_to_image(qr_matrix):
    """
    Convert the QR matrix (21x21 numpy array) to an image format.
    
    :param qr_matrix: A 21x21 numpy array representing the QR code.
    :return: A binary image (numpy array) that can be used for decoding.
    """
    qr_image = [[0 for i in range(len(qr_matrix))] for j in range(len(qr_matrix))]
    for i in range(len(qr_matrix)):
        for j in range(len(qr_matrix[0])):
            qr_image[i][j] = (1-qr_matrix[i][j])*255
    
    # Resize the image to make it larger (optional, but helps with decoding)
    qr_image = np.array(qr_image)

    qr_image = cv2.resize(qr_image, (210, 210), interpolation=cv2.INTER_NEAREST)
    
    return qr_image

def flatten_to_qr_matrix(flat):
    lenrows = int(len(flat)**0.5)
    matrix = [[0 for i in range(lenrows)] for j in range(lenrows)]
    for i in range(lenrows):
        for j in range(lenrows):
            matrix[i][j] = int(flat[i*lenrows+j])
    return matrix

# def audio_to_bitstring(wave_file, bit_duration=0.1, f0=440, f1=880, samplerate=44100):
#     """
#     Convert a frequency-modulated audio signal to a bitstring.
    
#     :param wave_file: The path to the WAV file to analyze.
#     :param bit_duration: Duration of each bit in seconds.
#     :param f0: Frequency for '0' in Hz.
#     :param f1: Frequency for '1' in Hz.
#     :param samplerate: Sampling rate in Hz.
#     :return: The decoded bitstring.
#     """
#     with wave.open(wave_file, 'r') as wav:
#         nframes = wav.getnframes()
#         data = wav.readframes(nframes)
#         audio = np.frombuffer(data, dtype=np.int16)
    
#     # Number of samples per bit
#     num_samples = int(samplerate * bit_duration)
    
#     # Decode the bitstring by analyzing the frequency of each segment
#     bitstring = ""
#     for i in range(0, len(audio), num_samples):
#         segment = audio[i:i+num_samples]
#         if len(segment) == 0:
#             break
        
#         # Perform a Fourier transform to find the frequency components
#         fft_result = np.fft.fft(segment)
#         freqs = np.fft.fftfreq(len(segment), 1/samplerate)
        
#         # Find the peak frequency
#         idx = np.argmax(np.abs(fft_result))
#         peak_freq = abs(freqs[idx])
        
#         # Determine if the frequency corresponds to '0' or '1'
#         if abs(peak_freq - f0) < abs(peak_freq - f1):
#             bitstring += '0'
#         else:
#             bitstring += '1'
    
#     return bitstring


import wave
import numpy as np
from scipy.signal import butter, lfilter

def butter_bandpass(lowcut, highcut, samplerate, order=5):
    nyquist = 0.5 * samplerate
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return b, a

def bandpass_filter(data, lowcut, highcut, samplerate, order=5):
    b, a = butter_bandpass(lowcut, highcut, samplerate, order=order)
    return lfilter(b, a, data)

def audio_to_bitstring(wave_file, bit_duration=0.1, f0=440, f1=880, samplerate=44100):
    """
    Convert a frequency-modulated audio signal to a bitstring.

    :param wave_file: The path to the WAV file to analyze.
    :param bit_duration: Duration of each bit in seconds.
    :param f0: Frequency for '0' in Hz.
    :param f1: Frequency for '1' in Hz.
    :param samplerate: Sampling rate in Hz.
    :return: The decoded bitstring.
    """
    with wave.open(wave_file, 'r') as wav:
        nframes = wav.getnframes()
        data = wav.readframes(nframes)
        audio = np.frombuffer(data, dtype=np.int16)

    # Number of samples per bit
    num_samples = int(samplerate * bit_duration)

    # Apply a bandpass filter to isolate the frequencies around f0 and f1
    filtered_audio = bandpass_filter(audio, lowcut=f0-100, highcut=f1+100, samplerate=samplerate)

    # Decode the bitstring by analyzing the frequency of each segment
    bitstring = ""
    for i in range(0, len(filtered_audio), num_samples):
        segment = filtered_audio[i:i+num_samples]
        if len(segment) == 0:
            break

        # Perform a Fourier transform to find the frequency components
        fft_result = np.fft.fft(segment)
        freqs = np.fft.fftfreq(len(segment), 1/samplerate)

        # Find the peak frequency
        idx = np.argmax(np.abs(fft_result))
        peak_freq = abs(freqs[idx])

        # Determine if the frequency corresponds to '0' or '1'
        if abs(peak_freq - f0) < abs(peak_freq - f1):
            bitstring += '0'
        else:
            bitstring += '1'

    return bitstring

print((audio_to_bitstring(audio_name)))

l = convert_matrix_to_image(flatten_to_qr_matrix(audio_to_bitstring(audio_name)))
Image.fromarray(l.astype(np.uint8)).save('qr.png')
from pyzbar.pyzbar import decode
from PIL import Image
decocdeQR = decode(Image.fromarray(l.astype(np.uint8)))
print(decocdeQR[0].data)