from crc_encode import crc_encode
from play import play
data = input()

generator = "1000000000000101"

crc = crc_encode(data=data, generator = "1000000000000101")

encoded_msg = crc + data

padding = "0011"

play(padding+encoded_msg)
