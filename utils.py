# Converts a given number into its binary string representation.
def int_to_binary(n, size=0):
    if n == 0:
        return '0'.rjust(size, '0')
    
    binary = ''
    while n > 0:
        binary = str(n % 2) + binary
        n = n // 2
        
    return binary.rjust(size, '0')

# Checks if the two provided bit strings share at least one bit set to '1' in the same position.
def have_common_bit(bit_string1, bit_string2):
    num1 = int(bit_string1, 2)
    num2 = int(bit_string2, 2)
    return (num1 & num2) != 0