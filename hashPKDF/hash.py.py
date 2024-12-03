import json

BS = 512//8    # 512 bits
MSG_SIZE_LEN = 8 
BLOCK_DIV = 16
IV = bytes([BS-i for i in range(BS)])

with open("aes.json", "r") as f:
    CONSTANTS = json.load(f)


# Utility functions
def pad(msg):
    l = len(msg)
    npad = BS - ((l + MSG_SIZE_LEN + 1) % BS)
    msg += b"\x01"
    msg += b"\x00" * npad
    msg += l.to_bytes(MSG_SIZE_LEN, "big", signed=False)
    assert (len(msg) % BS) == 0
    return msg

def block_to_words(block):
    return [block[i:i+(BS//BLOCK_DIV)] for i in range(0, BS, BS // BLOCK_DIV)]

def words_to_block(words):
    return b"".join(words)


# Operation on bytes
def bitand(a, b):
    assert len(a) == len(b)
    word = b""
    for i in range(len(a)):
        word += bytes([a[i] & b[i]])
    return word

def xor(a, b):
    assert len(a) == len(b)
    word = b""
    for i in range(len(a)):
        word += bytes([a[i] ^ b[i]])
    return word

def rot_left(word, d, bits=32):
    d = d % len(word)
    tail = word[d:]
    return tail + word[:d]

def rot_right(word, d, bits=32):
    d = d % len(word)
    head = word[:-d]
    return word[-d:] + head

def sub_word(word, inv=False):
    if inv:
        table = "inv_sbox"
    else:
        table = "sbox"

    result = b""
    for i in range(0, len(word)):
        result += bytes([CONSTANTS[table][word[i]]])
    return result

# State
class Compression:
    def __init__(self, block, prev_block):
        words = block_to_words(block)
        prev_words = block_to_words(prev_block)
        assert len(words) == BLOCK_DIV
        assert len(prev_words) == BLOCK_DIV
        self.words = words
        self.prev_words = prev_words

    def compress_round(self, i):
        # TODO    Step 3
        pass

    def get_result(self):
        return words_to_block(self.words[-BLOCK_DIV:])

def hash_block(block, prev):
    assert len(block) == BS
    assert len(prev) == BS

    # TODO    Step 2

    return cmp.get_result()

def truncate_cmp(hash):
    # TODO    Step 4
    word = b""
    return word

def custhash(message):
    # TODO Step 1
    return truncate_cmp(new_hash)

# TODO Step 4
h1 = custhash("Je suis une truite")
h2 = custhash("Je suis une truita")
print(h1.hex(), h2.hex())
