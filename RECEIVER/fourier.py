import wave
import numpy as np

def get_wav_duration(filename):
    with wave.open(filename, 'r') as wav_file:
        frames = wav_file.getnframes()
        rate = wav_file.getframerate()
        duration = frames / float(rate)
        return duration

def divide_list(lst, n):
    """
    Divides a list into n approximately equal parts.

    :param lst: The list to divide.
    :param n: The number of parts to divide the list into.
    :return: A list of n sublists.
    """
    # Calculate the size of each part
    k, m = divmod(len(lst), n)
    return [lst[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n)]

def inference(file_name = 'output.wav'):

    duration = round(get_wav_duration(file_name))

    with wave.open(file_name, 'rb') as wf:
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

    num = int(duration/0.5)
    no_chunks = 8

    array_audio_data = divide_list(audio_data, num)
    ans = ""

    for index in range(len(array_audio_data)):
        freqs = ([])
        chunks = divide_list(array_audio_data[index],no_chunks)

        for chunk_id in range(len(chunks)):
            # Perform Fourier Transform
            fft_result = np.fft.fft(chunks[chunk_id])
            frequencies = np.fft.fftfreq(len(chunks[chunk_id]), d=1/sample_rate)

            # Get the magnitude of the Fourier Transform
            magnitude = np.abs(fft_result)

            freqs.append(abs(int(frequencies[np.argmax(magnitude)])))

        freqs = np.array(freqs)
        # print(freqs)
        if sum(freqs <= 475)>no_chunks/2 :
            ans+="00"
            print("00")
        elif sum((475<=freqs) & (freqs <= 525))>no_chunks/2 :
            print("01")
            ans+="01"
        elif sum((525<=freqs) & (freqs <= 575))>no_chunks/2 :
            print("10")
            ans+="10"
        else:
            print("11")
            ans+="11"


    start = 0
    end = len(ans)
    prev = ans[0]
    for i in range(1,len(ans)):
        if ans[i]==prev=="1":
            start = i+1
            break
        prev = ans[i]

    # print("start ",start)
    return ans[start:start+(num-2)*2]
    # print("ans",ans)
