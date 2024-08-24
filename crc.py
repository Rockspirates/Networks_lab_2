def xor(dividend, divisor):
    # XOR operation between the dividend and divisor
    result = []
    print(len(dividend), len(divisor), dividend, divisor)
    for i in range(1, len(divisor)):
        if dividend[i] == divisor[i]:
            result.append('0')
        else:
            result.append('1')
    return ''.join(result)

def mod2div(dividend, divisor):
    # Number of bits to be XORed at a time
    pick = len(divisor)
    # Slicing the dividend to get the portion that matches the length of the divisor
    tmp = dividend[0:pick]
    while pick < len(dividend):
        print(tmp)
        if tmp[0] == '1':
            # Replace the dividend by the result of XOR and pull down the next bit
            tmp = xor(tmp, divisor) + dividend[pick]
        else:
            # If the first bit is '0', we XOR with '0...0' (equivalent to just appending the next bit)
            tmp = xor(tmp, '0' * len(divisor)) + dividend[pick]
        # Increment pick to move the window forward
        pick += 1
    
    # For the last n bits, we need to XOR with the divisor
    if tmp[0] == '1':
        tmp = xor(tmp, divisor)
    else:
        tmp = xor(tmp, '0' * len(divisor))
    
    return tmp

def crc_encode(data, generator):
    # Append zeros to the data string, length of generator minus 1
    appended_data = data + '0' * (len(generator) - 1)
    print(appended_data)
    # Perform division and get the CRC remainder
    remainder = mod2div(appended_data, generator)
    # The final CRC is the remainder of the division
    crc = remainder
    return crc

# Inputs
# generator = input("Enter CRC Generator (binary): ")
# message = input("Enter the Message String (binary): ")
generator = "1000000000000101"
message = "11000000101011011110"

# Calculating CRC
crc = crc_encode(message, generator)

# Output the CRC
print("Calculated CRC:", crc)
