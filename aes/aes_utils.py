
# https://github.com/francisrstokes/githublog/blob/main/2022/6/15/rolling-your-own-crypto-aes.md

import json


N_ROUNDS = 10
BLOCK_SIZE = 16
NCOL = 4    # SQRT(16)

with open("./aes.json", "r") as f:
    CONSTANTS = json.load(f)

class PaddingError(Exception):
    pass

# Add padding on the data
def pkcs_pad(data):
    nb = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    byte = nb.to_bytes(1, "big", signed=False)
    return data + (byte * nb)

# Remove padding from the data
def pkcs_unpad(data):
    nb = data[-1]
    suffix = data[-nb:]
    if not all([s == nb for s in suffix]):
        raise PaddingError("Invalid padding")
    return data[:-nb]

# XOR every number in 2 blocks (of same length)
def xor_word(a, b):
    assert len(a) == len(b)
    return [a[i] ^ b[i] for i in range(len(a))]

# Convert a list of bytes into a byte message
def block_to_bytes(block):
    return b"".join([x.to_bytes(1, "big", signed=False) for x in block])

# Convert a block into a list of block columns
def block_to_columns(block):
    return [list(block[i:i+4]) for i in range(0, BLOCK_SIZE, 4)]

# Convert a list of block columns back into a block
def columns_to_block(cols):
    res = []
    for col in cols:
        res.extend(col)
    return res

# Create a column rotation
def rot_column(col, inv=False):
    if inv:
        return [col[-1]] + col[:-1]
    else:
        return col[1:] + [col[0]]

# Add a constant to the column
def round_constant(nround, col):
    return [ x ^ CONSTANTS["round_cst"][nround][i] for (i, x) in enumerate(col) ]

# Substitute each byte of the word using the table in constants
def sub_word(word, inv=False):
    if inv:
        table = "inv_sbox"
    else:
        table = "sbox"

    for i in range(0, len(word)):
        word[i] = CONSTANTS[table][word[i]]

    return word

# Shift rows in a block
def shift_rows(block):       
    cols = block_to_columns(block)
    new_block = list()
    for i in range(NCOL):
        new_block.append(cols[i][0])
        new_block.append(cols[(i+1) % NCOL][1])
        new_block.append(cols[(i+2) % NCOL][2])
        new_block.append(cols[(i+3) % NCOL][3])
    return new_block

# Inverse the shift rows in a block
def inv_shift_rows(block):            
    cols = block_to_columns(block)
    new_block = list()
    for i in range(NCOL):
        new_block.append(cols[i][0])
        new_block.append(cols[(i+15) % NCOL][1])
        new_block.append(cols[(i+14) % NCOL][2])
        new_block.append(cols[(i+13) % NCOL][3])
    return new_block

# Perform galois multiplication on 2 bytes
def galois_mult(a, b):
    result = 0
    shift_greater_255 = 0
    for i in range(0, 8):
        if b & 1:
            result ^= a

        shift_greater_255 = a & 0x80
        a <<= 1
        if shift_greater_255 > 0:
            a ^= 0x11b
        b >>=1
    return result

# Mix / Unmix columns with galois multiplications
def mix_column(col, inv=False):
    if not inv:
        res = [
            galois_mult(0x02, col[0]) ^ galois_mult(0x03, col[1]) ^ col[2] ^ col[3],
            col[0] ^ galois_mult(0x02, col[1]) ^ galois_mult(0x03, col[2]) ^ col[3],
            col[0] ^ col[1] ^ galois_mult(0x02, col[2]) ^ galois_mult(0x03, col[3]),
            galois_mult(0x03, col[0]) ^ col[1] ^ col[2] ^ galois_mult(0x02, col[3]),
            ]
    else:
        res = [
            galois_mult(0x0e, col[0]) ^ galois_mult(0x0b, col[1]) ^ galois_mult(0x0d, col[2]) ^ galois_mult(0x09, col[3]),
            galois_mult(0x09, col[0]) ^ galois_mult(0x0e, col[1]) ^ galois_mult(0x0b, col[2]) ^ galois_mult(0x0d, col[3]),
            galois_mult(0x0d, col[0]) ^ galois_mult(0x09, col[1]) ^ galois_mult(0x0e, col[2]) ^ galois_mult(0x0b, col[3]),
            galois_mult(0x0b, col[0]) ^ galois_mult(0x0d, col[1]) ^ galois_mult(0x09, col[2]) ^ galois_mult(0x0e, col[3]),
            ]
    return res

def generate_round_keys(key):
    key_rounds = [key]

    col = block_to_columns(key)

    for n in range(N_ROUNDS):
        key = list()
        tmp = round_constant(n, sub_word(rot_column(col[-1])))
        col1 = xor_word(col[0], tmp)
        key.extend(col1)
        col2 = xor_word(col1, col[1])
        key.extend(col2)
        col3 = xor_word(col2, col[2])
        key.extend(col3)
        col4 = xor_word(col3, col[3])
        key.extend(col4)
        key_rounds.append(key)
        col = [ col1, col2, col3, col4 ]
    return key_rounds

def aes_round(block, round_keys, round):
    block = sub_word(block)
    block = shift_rows(block)
    if round < N_ROUNDS:
        block = block_to_columns(block)
        block = columns_to_block([mix_column(col) for col in block])
    block = xor_word(block, round_keys[round])
    return block

def aes_inv_round(block, round_keys, round):
    block = inv_shift_rows(block)
    block = sub_word(block, inv=True)
    block = xor_word(block, round_keys[round])

    if round > 0: #N_ROUNDS:
        block = [mix_column(col, inv=True) for col in block_to_columns(block)]
        block = columns_to_block(block)

    return block
