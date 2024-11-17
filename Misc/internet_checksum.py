a = 0b1001_1011_0011_0100
b = 0b1011_0100_1000_1101
sum = a + b 

if sum > 0xFFFF: 
    sum = (sum & 0xFFFF) + 1  

checksum = ~sum & 0xFFFF  

print(f"Sum: \n{sum:016b}")
print(f"Checksum: \n{checksum:016b}")

'''
Output:
Sum: 
0001100101111001
Checksum: 
1110011010000110
'''