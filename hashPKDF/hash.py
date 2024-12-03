from filecmp import cmp
from hash_utils import *  # Import the utility functions

"""
Fichier avec les fonctions de base en TODO
"""
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
    #block 1
    prev_block = IV
    
    # padding ++
    padded_msg = pad(message.encode("utf-8")) 
    
    # loop blocks
    for i in range(0, len(padded_msg), BS):
        block = padded_msg[i:i + BS]
        prev_block = hash_block(block, prev_block)
        
    todolater = null
    return todolater


# TODO Step 4
h1 = custhash("Je suis une truite")
h2 = custhash("Je suis une truita")
print(h1.hex(), h2.hex())
