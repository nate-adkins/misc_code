def modulo2_division(data, generator):
    data = [int(bit) for bit in data]
    generator = [int(bit) for bit in generator]
    data += [0] * (len(generator) - 1)
    for i in range(len(data) - len(generator) + 1):
        if data[i] == 1:
            for j in range(len(generator)):
                data[i + j] ^= generator[j]

    remainder = data[-(len(generator) - 1):]
    return ''.join(map(str, remainder))

def valid_crc(data, generator, remainder):
    data = [int(bit) for bit in data]
    generator = [int(bit) for bit in generator]
    remainder = [int(bit) for bit in remainder]
    data_with_remainder = data + remainder
    check_remainder = modulo2_division(data_with_remainder, generator)
    return all(bit == '0' for bit in check_remainder)

D = "10011111"
G = "1001"     

R = modulo2_division(D, G)
print(f"Computed CRC bits: {R}")

print(f"CRC verification result: {'Valid' if valid_crc(D, G, R) else 'Invalid'}")
