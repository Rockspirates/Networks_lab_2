import pyaudio
import wave
from struct import pack

def record(outputfile):
    chunk = 1024
    format = pyaudio.paInt16
    channels = 2
    rate = 44100 #in hertz
    duration = 44 #5 seconds
    p = pyaudio.PyAudio()
    stream = p.open(format=format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)
    print("Recording has started...")
    frames = []
    for i in range(0,int(rate/chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(outputfile, "wb")
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b"".join(frames))
    wf.close()

record("aditya.wav")

    