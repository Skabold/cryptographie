import os
import json
import base64

# https://github.com/francisrstokes/githublog/blob/main/2022/6/15/rolling-your-own-crypto-aes.md

N_ROUNDS = 10
BLOCK_SIZE = 16
NCOL = 4    # SQRT(16)

with open("aes.json", "r") as f:
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
def shift_rows(block):        # OK
    cols = block_to_columns(block)
    new_block = list()
    for i in range(NCOL):
        new_block.append(cols[i][0])
        new_block.append(cols[(i+1) % NCOL][1])
        new_block.append(cols[(i+2) % NCOL][2])
        new_block.append(cols[(i+3) % NCOL][3])
    return new_block

# Inverse the shift rows in a block
def inv_shift_rows(block):            # OK
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

### Début du TP
# Validate avec https://www.samiam.org/key-schedule.html
def generate_round_keys(key):        # OK
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

class AES:
    def __init__(self, key=None):
        if key is None:
            key = os.urandom(BLOCK_SIZE)
        self.key = key

    def encrypt(self, data):
        """
        Encrypt the data using AES.

        Parameters:
        data (dict): A dictionary containing the data to encrypt.

        Returns:
        bytes: The encrypted data.
        """
        data_bytes = json.dumps(data).encode('utf-8')
        data_bytes = pkcs_pad(data_bytes)

        iv = os.urandom(BLOCK_SIZE)

        data_bytes = list(data_bytes)
        output = b""

        round_keys = generate_round_keys(self.key)
        for b in range(0, len(data_bytes), BLOCK_SIZE):
            if b == 0:
                chainblock = iv
            else:
                chainblock = output[-BLOCK_SIZE:]
            block = data_bytes[b:b+BLOCK_SIZE]

            block = xor_word(block, chainblock)
            block = xor_word(block, round_keys[0])
            for round in range(0, N_ROUNDS):
                round += 1
                block = aes_round(block, round_keys, round)
                assert len(block) == BLOCK_SIZE
            output += block_to_bytes(block)

        return iv + output

    def decrypt(self, data):
        """
        Decrypt the data using AES.

        Parameters:
        data (bytes): The encrypted data to decrypt.

        Returns:
        dict: The decrypted data as a dictionary.
        """
        round_keys = generate_round_keys(self.key)

        lblock = data[-BLOCK_SIZE:]
        lblock = xor_word(lblock, round_keys[-1])
        for round in range(1, N_ROUNDS+1):
            lblock = aes_inv_round(lblock, round_keys, N_ROUNDS - round)

        output = b""
        for b in range(BLOCK_SIZE, len(data), BLOCK_SIZE):
            block = data[-(b+BLOCK_SIZE):-b]

            output = block_to_bytes(xor_word(lblock, list(block))) + output

            lblock = block
            lblock = xor_word(lblock, round_keys[-1])
            for round in range(1, N_ROUNDS+1):
                lblock = aes_inv_round(lblock, round_keys, N_ROUNDS - round)

        output = pkcs_unpad(output)
        return json.loads(output.decode('utf-8'))

    def export(self):
        """Export the AES key as a base64 encoded string."""
        return base64.b64encode(self.key).decode('utf-8')

    @classmethod
    def from_export(cls, encoded_key):
        """Create an AES instance from a base64 encoded key."""
        key = base64.b64decode(encoded_key)
        return cls(key)

# Exemple d'utilisation
cipher = AES(key=bytearray.fromhex("2b7e151628aed2a6abf7158809cf4f3c"))

data = {'message': 'Hello, World!'}
encrypted_data = cipher.encrypt(data)
print(f"Encrypted data: {encrypted_data}")
decrypted_data = cipher.decrypt(encrypted_data)
print(f"Decrypted data: {decrypted_data}")


# Exemple d'utilisation use the key from a friend and his message
encoded_key = "56dzKUA2T1LqpleJRKfUzA=="
encrypted_data = b'\xdd\xcb\xbc_k\x91A\x91pw\xe9\x8f\xe0\xe4\xcf\x13\x87\xd0M\xae\xca1\xffJbz\x0b\xb5,~\xe3h\xe6\x17\x8b\xe7S\xa2\x03\xcc\xa4\x08hj\xc4a6a'

# Importer la clé AES
cipher = AES.from_export(encoded_key)
# Déchiffrer le message encodé
decrypted_data = cipher.decrypt(encrypted_data)
print(f"Decrypted data : {decrypted_data}")
