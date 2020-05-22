def dec_to_hex(value):
    done = False
    hex_values = {
        10: 'A',
        11: 'B',
        12: 'C',
        13: 'D',
        14: 'E',
        15: 'F'
    }

    result = ''
    while not done:
        quotient = value // 16
        remainder = value % 16
        if remainder > 9:
            result += hex_values[remainder]
        else:
            result += str(remainder)

        if quotient == 0:
            done = True
        else:
            value = quotient

    return result

print(dec_to_hex(int(input('Enter a decimal value to be converted to hexadecimal: '))))
# print('35631 converted to hexadecimal is', dec_to_hex(35631))

def dec_to_bin(value):
    if value == 0:
        return ''
    else:
        return dec_to_bin(value // 2) + str(value % 2)

print(dec_to_bin(int(input('Enter a decimal number to be converted to binary: '))))
# print('24 converted to binary is', dec_to_bin(24))

# def bin_to_hex(value):
#     one_table = [1,2,4,8]
#     sixteen_table = [16,32,64,128]
#     two_fiddy_table = [256,512,1024,2048]

