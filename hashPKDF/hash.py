from filecmp import cmp
from hash_utils import *  # Import the utility functions
import time


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
        # Sélection des mots
        word1 = self.words[i]
        word2 = self.prev_words[(i)]
        word3 = self.words[(i + 2)]
        word4 = self.prev_words[(i + 2)]

        # mélange
        mixed_word_1 = xor(word1, word2)
        mixed_word_2 = xor(word3, word4)
        mixed_word_f = xor(mixed_word_1, mixed_word_2)

        self.words.append(mixed_word_f)

    def get_result(self):
        return words_to_block(self.words[-BLOCK_DIV:])


def hash_block(block, prev):
    assert len(block) == BS
    assert len(prev) == BS

    cmp = Compression(block, prev)
    N = 10
    for i in range(N):
        cmp.compress_round(i)

    return cmp.get_result()

def truncate_cmp(hash):
    return xor(hash, IV)


def custhash (message):
    message = message.encode('utf-8')
    padded_message = pad(message)
    prev_block = IV
    new_hash = b""

    for i in range(0, len(padded_message), BS):
        block = padded_message[i:i + BS]
        prev_block = hash_block(block, prev_block)
        new_hash += prev_block

    return truncate_cmp(new_hash)


def test_hash_function():
    h1 = custhash ("Je suis une truite")
    h2 = custhash ("Je suis une truita")
    print("Hash 1:", h1.hex())
    print("Hash 2:", h2.hex())
    assert h1 != h2, "The hashes should be different"

    # Measure execution time
    start_time = time.time()
    for _ in range(100):
        custhash ("Je suis une truite")
    end_time = time.time()
    avg_time = (end_time - start_time) / 100
    print(f"Average time per block: {avg_time * 1000:.2f} ms")
