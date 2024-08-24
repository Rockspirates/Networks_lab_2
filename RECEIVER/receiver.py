from filters import high_pass_filter
from filters  import low_pass_filter
from record import record
from fourier import inference
from crc_decode import find_errors

record()
high_pass_filter()
low_pass_filter()
signal = inference()

print(signal)
generator = "1000000000000101"

crc = signal[:len(generator)-1]
msg = signal[len(generator)-1:]

print(msg,crc)

final_ans = find_errors(code_word=msg+crc)[:len(msg)]

print(final_ans)


