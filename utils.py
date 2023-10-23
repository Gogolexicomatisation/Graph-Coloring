# Change a number to its binary string version
def int_to_binary(n, size=0):
    if n == 0:
        return '0'.rjust(size, '0')
    
    binary = ''
    while n > 0:
        binary = str(n % 2) + binary
        n = n // 2
        
    return binary.rjust(size, '0')

def have_common_bit(bit_string1, bit_string2):
    # Convert bitstrings to integers
    num1 = int(bit_string1, 2)
    num2 = int(bit_string2, 2)
    
    # Check if the result of the AND operation is not zero
    return (num1 & num2) != 0