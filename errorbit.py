def xor(dividend, divisor):
    result = []
    for i in range(1, len(divisor)):
        if dividend[i] == divisor[i]:
            result.append('0')
        else:
            result.append('1')
    return ''.join(result)

def mod2div(dividend, divisor):
    pick = len(divisor)
    tmp = dividend[0:pick]
    
    while pick < len(dividend):
        if tmp[0] == '1':
            tmp = xor(tmp, divisor) + dividend[pick]
        else:
            tmp = xor(tmp, '0' * len(divisor)) + dividend[pick]
        pick += 1
    
    if tmp[0] == '1':
        tmp = xor(tmp, divisor)
    else:
        tmp = xor(tmp, '0' * len(divisor))
    
    return tmp

def crc_decode(data, generator):
    appended_data = data + '0' * (len(generator) - 1)
    remainder = mod2div(appended_data, generator)
    return remainder

def onebit_detect(code_word, generator):
    code_list = list(code_word)  # Convert string to list for mutability
    for i in range(len(code_list)):
        code_list[i] = '0' if code_list[i] == '1' else '1'
        if mod2div(''.join(code_list), generator) == '0'*15:
            return i
        code_list[i] = '0' if code_list[i] == '1' else '1'
    return -1

def twobit_detect(code_word, generator):
    code_list = list(code_word)  # Convert string to list for mutability
    for i in range(len(code_list)):
        for j in range(i + 1, len(code_list)):
            code_list[i] = '0' if code_list[i] == '1' else '1'
            code_list[j] = '0' if code_list[j] == '1' else '1'
            if mod2div(''.join(code_list), generator) == '0'*15:
                return [i, j]
            code_list[i] = '0' if code_list[i] == '1' else '1'
            code_list[j] = '0' if code_list[j] == '1' else '1'
    return [-1, -1]

code_word = "11000000101011011110010000000111110"
generator = "1000000000000101"

if mod2div(code_word, generator) == '0'*15:
    print("No error")
else:
    bit = onebit_detect(code_word, generator)
    if bit != -1:
        print("One bit error present at:", bit)
    else:
        bits = twobit_detect(code_word, generator)
        if bits != [-1, -1]:
            print("Two bits error present at:", bits[0], bits[1])
        else:
            print("More than two-bit error or uncorrectable error")
