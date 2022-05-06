# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import re

# reformats the key to work with plaintext
def reformat_key(string, key):
    key = list(key)
    if len(string) == len(key):
        return(key)
    else:
        for i in range(len(string) -
                       len(key)):
            key.append(key[i % len(key)])
    return("" . join(key))

# preforms a vigenere cypher encryption
def vigenere_encrypt(plain_text,key):
    cipher_text = []
    for i in range(len(plain_text)):
        x = (ord(plain_text[i]) +
             ord(key[i])) % 26
        x += ord('A')
        cipher_text.append(chr(x))
    return ("".join(cipher_text))

# puts the modified plaintext into blocks of 4 and adds any needed padding
def to_blocks(plain_text):
    many_blocks = []
    block_text = []
    # if not a 4x4 block then add padding
    if len(plain_text)% 16 != 0:
        padding = 16 - len(plain_text)% 16
        for j in range(padding):
            plain_text += 'A'
    # otherwise append the 4x4 blocks to a list
    for i in range(0, len(plain_text), 4):

        block_text.append(plain_text[i: i + 4])

    for i in range(0,len(block_text),4):
        many_blocks.append(block_text[i: i+4])
    return many_blocks

# rotates text for row shifts
def left_rotate(text,num):
    tmp = text[num:] + text[0: num]
    return tmp

# shifting rows function
def shift_rows(block_text):

    for i in range(len(block_text)):
        for j in range(len(block_text[i])):
            for k in range(len(block_text[i][j])):
                # shift over 1 if in column[1]
                if k == 1:
                    block_text[i][j][k] = left_rotate(block_text[i][j][k], k)
                # shift over 2 if in column[2]
                elif k == 2:
                    block_text[i][j][k] = left_rotate(block_text[i][j][k], k)
                # shift over 3 if in column[1]
                elif k == 3:
                    block_text[i][j][k] = left_rotate(block_text[i][j][k], k)

    return block_text


def parity_bit(block_text):

    for i in range(len(block_text)):
        for j in range(len(block_text[i])):
            for k in range(len(block_text[i][j])):
                # takes hex values for every 4 letters into a list
                hex_values = []
                for g in range(len(block_text[i][j][k])):
                    #converts letter to binary
                    bin_val = bin(ord(block_text[i][j][k][g])).replace('0b','')
                    # checks number of 1s in binary value
                    count = 0
                    for u in bin_val:
                        if u =='1':
                            count += 1

                    temp = list(bin_val)
                    temp.insert(0,'0')
                    if count % 2 == 0:
                        bin_val = "".join(temp)
                        hex_values.append(hex(int(bin_val, 2)).replace('0x',''))
                    else:
                        if temp[0] == '1':
                            temp[0] = '0'
                        else:
                            temp[0] = '1'
                        bin_val = "".join(temp)

                        hex_values.append(hex(int(bin_val, 2)).replace('0x',''))
                    if len(hex_values) == 4:

                        block_text[i][j][k] = hex_values

    return block_text

# preforms 4x4 matrix multiplication with galios block
def matrix_mul(sub_block):
    # initialize galios block
    galios_block = [[2, 3, 1, 1], [1, 2, 3, 1], [1, 1, 2, 3], [3, 1, 1, 2]]
    # initialize empty 4x4 matrix
    matrix = [['' for _ in range(4)] for _ in range(4)]
    for i in range(len(galios_block)):
        for j in range(len(sub_block[0])):
            # hex values to be added are put into a lisy
            add_block = []
            for k in range(len(sub_block)):

                # checks galios conditions
                if galios_block[i][k] == 2:
                    temp = bin(int(sub_block[k][j], 16))
                    # checks for overflow
                    if temp[3] == '1':
                        val = bin((int(sub_block[k][j], 16) << 1 ^ int('00011011', 2)))[3:]
                    else:
                        val = bin((int(sub_block[k][j], 16) << 1))[2:]

                    add_block.append(val)

                # checks galios conditions
                elif galios_block[i][k] == 3:
                    temp = bin(int(sub_block[k][j], 16))

                    # checks for overflow
                    if temp[3] == '1':
                        val = bin((int(sub_block[k][j], 16) << 1) ^ int(sub_block[k][j], 16) ^ int('00011011',2))[3:]
                    else:
                        val = bin((int(sub_block[k][j], 16) << 1) ^ int(sub_block[k][j], 16))[2:]

                    add_block.append(val)
                # checks galios conditions
                else:
                    add_block.append(bin(int(sub_block[k][j], 16))[2:])

                # when all values visited on the galios block xor all the given values together to get the column
                if k == 3:
                    matrix[i][j] = hex(int(add_block[0],2) ^ int(add_block[1],2) ^ int(add_block[2],2)^int(add_block[3],2))[2:]

    return matrix


def mix_cols(block_text):

    for x in range(len(block_text)):
        # goes through every 4x4 matrix block and preforms matrix multiplication
        for i in range(len(block_text[x])):
            block_text[x][i] = matrix_mul(block_text[x][i])


def write_blocks(out_file, block_text):

    # simply writes the more complex matrices to the file
    for i in range(len(block_text)):
        for j in range(len(block_text[i])):
            for k in range(len(block_text[i][j])):
                if len(block_text[i][j][k][0])!=2:
                    if k % 4 == 0 :
                        out_file.write('\n')
                for p in range(len(block_text[i][j][k])):
                    if p % 4 == 0:
                        out_file.write('\n')
                    if len(block_text[i][j][k][p])==2:
                        out_file.write(block_text[i][j][k][p] + ' ')
                    else:
                        out_file.write(block_text[i][j][k][p])


def encryption(read_plain, read_key, out_file):

    processed_plain = []
    vigenere_cyphertxt = []
    block_text = []

    for i in read_plain:
        punct = re.sub(r'[^\w\s]', '', i)
        processed_plain.append(punct.replace(" ", ""))

    # write output to file
    out_file.writelines("Preprocessing: \n")
    out_file.writelines(processed_plain)

    for j in processed_plain:
        key = reformat_key(j, read_key)
        vigenere_cyphertxt.append(vigenere_encrypt(j, key))

    # write output to file
    out_file.write("\n\n")
    out_file.write("Substitution: \n")
    out_file.writelines(vigenere_cyphertxt)

    for k in vigenere_cyphertxt:
        block_text.append(to_blocks(k))

    # write output to file
    out_file.write("\n\n")
    out_file.write("Padding: ")
    write_blocks(out_file,block_text)

    # write output to file
    shift_rows(block_text)
    out_file.write("\n\n")
    out_file.write("Shift rows: ")
    write_blocks(out_file,block_text)

    # write output to file
    parity_bit(block_text)
    out_file.write("\n\n")
    out_file.write("Parity bit:")
    write_blocks(out_file,block_text)

    # write output to file
    mix_cols(block_text)
    out_file.write("\n\n")
    out_file.write("Mixed columns: ")
    write_blocks(out_file, block_text)
    out_file.close()


def read_my_file():
    plain_name = input("enter the plain text file name : ")
    key_name = input("enter the key file name : ")
    out_name = input("enter the output file name : ")
    try:
        plain_file = open(plain_name, "r")
        read = plain_file.readlines()
        read_plain = []

        for i in read:
            if len(i.rstrip()) == 0:
                continue
            else:
                read_plain.append(i)
    except:
        print('could not open the plain text file: ')

    try:
        key_file = open(key_name, "r")
        read_key = key_file.readlines()

    except:
        print('could not open the key text file: ')
    try:
        out_file = open(out_name,"w")
    except:
        print('could not open the output text file: ')

    encryption(read_plain, read_key, out_file)
    res = open(out_name, 'r')
    for i in res.readlines():
        print(i.rstrip())
    res.close()
    print("Contents successfully encrypted and written to the output file!")







    # Use a breakpoint in the code line below to debug your script.
    # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    read_my_file()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
