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
        # Sélection des "words" en fonction du round
        word1 = self.words[i % BLOCK_DIV]
        word2 = self.prev_words[(i + 1) % BLOCK_DIV]
        word3 = self.words[(i + 2) % BLOCK_DIV]
        word4 = self.prev_words[(i + 3) % BLOCK_DIV]

        # Création de l'algorithme de mélange
        mixed_word = sub_word(word1)
        mixed_word = xor(mixed_word, word2)
        mixed_word = bitand(mixed_word, word3)
        mixed_word = rot_left(mixed_word, i % 4)
        mixed_word = xor(mixed_word, word4)
        mixed_word = rot_right(mixed_word, (i + 1) % 4)

        # Ajout du nouveau "word" à la liste self.words
        self.words.append(mixed_word)

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


def my_hash(message):
    message = message.encode('utf-8')
    padded_message = pad(message)
    prev_block = IV
    new_hash = b""

    for i in range(0, len(padded_message), BS):
        block = padded_message[i:i + BS]
        prev_block = hash_block(block, prev_block)
        new_hash += prev_block

    return truncate_cmp(new_hash)


# TODO Step 4
def test_hash_function():
    h1 = my_hash("Je suis une truite")
    h2 = my_hash("Je suis une truita")
    print("Hash 1:", h1.hex())
    print("Hash 2:", h2.hex())
    assert h1 != h2, "The hashes should be different"

    # Measure execution time
    start_time = time.time()
    for _ in range(100):
        my_hash("Je suis une truite")
    end_time = time.time()
    avg_time = (end_time - start_time) / 100
    print(f"Average time per block: {avg_time * 1000:.2f} ms")


test_hash_function()
