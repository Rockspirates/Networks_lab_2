import pyaudio
import wave
from array import array
from struct import pack

def play(file):
    chunk = 1024
    #this will open the audio file and start reading it in the form of bits
    wf = wave.open(file, 'rb')
    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    
    data = wf.readframes(chunk)
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(chunk)
    
    stream.stop_stream()
    stream.close()
    p.terminate()


play("file_example_WAV_1MG.wav")