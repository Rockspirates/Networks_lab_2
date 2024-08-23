import wave 
import numpy as np 
import simpleaudio as sa 
 
# Open the WAV file 
# with wave.open('file_example_WAV_1MG.wav', 'r') as wav: 
#     # Get the audio parameters 
#     params = wav.getparams() 
#     channels, sampwidth, framerate, nframes = params[:4] 
 
#     # Read the audio data 
#     data = wav.readframes(nframes) 
 
# # Convert the data to a NumPy array 
# audio = np.frombuffer(data, dtype=np.int16) 
# print(audio[:10], len(audio), len(np.unique(audio)))
 
# # Create a simpleaudio player and play the audio 
# play_obj = sa.play_buffer(audio, channels, sampwidth, framerate) 
# play_obj.wait_done() 


######################################################################

import wave
import numpy as np
import simpleaudio as sa

# Create the binary pattern as a numpy array
# '0' is treated as the minimum amplitude, and '1' as the maximum amplitude.
audio = np.concatenate([
    np.zeros(5000, dtype=int),  # 10000 elements of 1
    np.ones(5000, dtype=int),  # 10000 elements of 2
    np.zeros(5000, dtype=int),  # 10000 elements of 1
    np.ones(5000, dtype=int), 
    np.zeros(5000, dtype=int),  # 10000 elements of 1
    np.ones(5000, dtype=int), 
    np.zeros(5000, dtype=int),  # 10000 elements of 1
    np.ones(5000, dtype=int), 
    np.zeros(5000, dtype=int),  # 10000 elements of 1
    np.ones(5000, dtype=int), 
])

channels = 1
sampwidth = 2  # 16-bit audio has a sample width of 2 bytes
framerate = 44100  # Standard sampling rate

# Play the audio
play_obj = sa.play_buffer(audio, channels, sampwidth, framerate)
play_obj.wait_done()
